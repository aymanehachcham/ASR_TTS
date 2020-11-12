
from rest_framework.response import Response
from rest_framework.decorators import api_view
import nemo
import nemo_asr
import time
from . models import *
@api_view(['POST'])
def convert(request):
    """
    ** Create new sound recognation object by convert audio to text .


    ** Use Case Exemple of Post:

                {

                    "audio":"base64 format",

                }



    """
    import json
    from ruamel.yaml import YAML
    import nemo
    import nemo_asr
    import IPython.display as ipd
    MODEL_YAML = "/home/docker/app/ai_models/quartznet15x5.yaml"
    CHECKPOINT_ENCODER = "/home/docker/app/ai_models/JasperEncoder-STEP-243800.pt"
    CHECKPOINT_DECODER = "/home/docker/app/ai_models/JasperDecoderForCTC-STEP-243800.pt"
    ENABLE_NGRAM = False
    yaml = YAML(typ="safe")
    with open(MODEL_YAML) as f:
        jasper_model_definition = yaml.load(f)
    labels = jasper_model_definition['labels']
    neural_factory = nemo.core.NeuralModuleFactory(
        placement=nemo.core.DeviceType.CPU,
        backend=nemo.core.Backend.PyTorch)
    data_preprocessor = nemo_asr.AudioToMelSpectrogramPreprocessor(factory=neural_factory)
    jasper_encoder = nemo_asr.JasperEncoder(
        jasper=jasper_model_definition['JasperEncoder']['jasper'],
        activation=jasper_model_definition['JasperEncoder']['activation'],
        feat_in=jasper_model_definition['AudioToMelSpectrogramPreprocessor']['features'])
    jasper_encoder.restore_from(CHECKPOINT_ENCODER, local_rank=0)
    jasper_decoder = nemo_asr.JasperDecoderForCTC(
        feat_in=1024,
        num_classes=len(labels))
    jasper_decoder.restore_from(CHECKPOINT_DECODER, local_rank=0)
    greedy_decoder = nemo_asr.GreedyCTCDecoder()

    def wav_to_text(manifest, greedy=True):
        from ruamel.yaml import YAML
        yaml = YAML(typ="safe")
        with open(MODEL_YAML) as f:
            jasper_model_definition = yaml.load(f)
        labels = jasper_model_definition['labels']
        data_layer = nemo_asr.AudioToTextDataLayer(
            shuffle=False,
            manifest_filepath=manifest,
            labels=labels, batch_size=1)
        audio_signal, audio_signal_len, _, _ = data_layer()
        processed_signal, processed_signal_len = data_preprocessor(
            input_signal=audio_signal,
            length=audio_signal_len)
        encoded, encoded_len = jasper_encoder(audio_signal=processed_signal,
                                              length=processed_signal_len)
        log_probs = jasper_decoder(encoder_output=encoded)
        predictions = greedy_decoder(log_probs=log_probs)

        if ENABLE_NGRAM:
            print('Running with beam search')
            beam_predictions = beam_search_with_lm(
                log_probs=log_probs, log_probs_length=encoded_len)
            eval_tensors = [beam_predictions]

        if greedy:
            eval_tensors = [predictions]

        tensors = neural_factory.infer(tensors=eval_tensors)
        if greedy:
            from nemo_asr.helpers import post_process_predictions
            prediction = post_process_predictions(tensors[0], labels)
        else:
            prediction = tensors[0][0][0][0][1]
        return prediction

    def create_manifest(file_path):
        # create manifest
        manifest = dict()
        manifest['audio_filepath'] = file_path
        manifest['duration'] = 18000
        manifest['text'] = 'todo'
        with open(file_path + ".json", 'w') as fout:
            fout.write(json.dumps(manifest))
        return file_path + ".json"
    data = request.FILES['audio']
    path = "media/"+data.name
    audio = Song.objects.create(audio_file=data)
    transcription = wav_to_text(create_manifest(audio.audio_file.path))

    return Response({'Output':transcription})

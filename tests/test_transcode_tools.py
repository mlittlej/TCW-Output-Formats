import tcw_transcode_tools
import os.path
import pytest


def test_output_filename_sanitiser():
    # This file doesn't need to exist - it's just an example path to see whether the sanitisaton works
    test_file = "/home/flamekebab/stereo_test.wav"
    assert tcw_transcode_tools.output_filename_sanitiser(test_file) == "stereo_test"


# A simple test encode
def test_opus_mono_transcode():
    test_file = "tests/stereo_test.wav"
    tcw_transcode_tools.ffmpeg_audio_transcode(
        test_file, "tests/", "mono_test", "opus", "24000", "1"
    )

    assert os.path.isfile("tests/mono_test.opus")
    os.remove("tests/mono_test.opus")


# Then we can test a whole host of different options to see if any break
transcoding_tests = [
    ("mono_test", "opus", "24000", "1"),
    ("stereo_test", "opus", "2400", "2"),
    ("mono_test", "mp3", "5.5", "1"),
    ("mono_test", "ogg", "1", "1"),
    ("stereo_test", "m4a", "3", "2"),
]

# Parametrize those badboys:
@pytest.mark.parametrize("output_file, codec, q_or_b, channels", transcoding_tests)
def test_transcoding(output_file, codec, q_or_b, channels):
    test_file = "tests/stereo_test.wav"
    tcw_transcode_tools.ffmpeg_audio_transcode(
        test_file, "tests/", output_file, codec, q_or_b, channels
    )

    # It might seem silly checking whether the file exists or not but in this context ffmpeg either works or doesn't.
    # We could of course get clever and use ffmpeg to probe the files but I dread to think what that documentation looks like
    assert os.path.isfile(f"tests/{output_file}.{codec}")

    # After we've checked whether the files are generated we can delete them to tidy up
    os.remove(f"tests/{output_file}.{codec}")

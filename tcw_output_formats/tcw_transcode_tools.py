#!/usr/bin/env python3
import ffmpeg


def output_filename_sanitiser(dirty_filename):
    # The filenames we output when done transcoding use the original filenames but chop off the extension

    # Grab the name of the file for the finished audio files, split it into a list, keep only the last entry - the file
    dirty_path_list = dirty_filename.split("/")
    filename_with_extension = dirty_path_list[-1]

    # We're going to need to trim the string but it's unclear how long it is (e.g. "mp3" vs. "opus")
    file_extension = filename_with_extension.split(".")

    # Then we grab the final element in the resultant list and add a full stop to it
    file_extension = f".{file_extension[-1]}"

    # Then we remove the suffix from the string
    return filename_with_extension.removesuffix(file_extension)


def ffmpeg_audio_transcode(
    audio_input,
    output_path_body,
    just_output_file_name,
    codec,
    quality_or_bitrate,
    audio_channels,
):

    # Load the file into ffmpeg
    input_stream = ffmpeg.input(audio_input)

    # This isn't necessary but it makes things a bit more readable in the trouble spot further down
    full_output_path = f"{output_path_body}/{just_output_file_name}.{codec}"

    # The KWARGS thing means we're going to need to figure out how the codec details need to be formatted:
    if codec == "opus":
        stream = ffmpeg.output(
            input_stream,
            full_output_path,
            ac=audio_channels,
            audio_bitrate=quality_or_bitrate,
        )
    elif codec == "mp3" or codec == "m4a" or codec == "ogg":
        # I feel a bit bad for using "m4a" here when the codec is named AAC but that's me being pedantic
        stream = ffmpeg.output(
            input_stream, full_output_path, ac=audio_channels, q=quality_or_bitrate
        )
    else:
        print("\n\n\ncodec not supported\n\n\n")

    ffmpeg.run(stream)

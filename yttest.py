
from dl_yt_subtitles import download_youtube_video_info, extract_and_concat_subtitle_text, find_first_youtube_url, extract_title, extract_description

video_metadata= download_youtube_video_info(find_first_youtube_url("https://www.youtube.com/watch?v=OG0AvwM_QAI"))
print(video_metadata)
subtitle_text= extract_and_concat_subtitle_text(str(video_metadata))
print(subtitle_text)
print(len(subtitle_text))

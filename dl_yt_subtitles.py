import yt_dlp
import re

def download_youtube_video_info(url):
    # Configuration for yt-dlp
    ydl_opts = {
        'writesubtitles': True,       # Download subtitles if available
        'writeautomaticsub': True,    # Download automatic subtitles if no others are available
        'subtitleslangs': ['en'],     # Preferred languages for the subtitles
        'skip_download': True,        # Skip downloading the video, only metadata and subtitles
        'quiet': True,                # Reduce output
        'outtmpl': 'subtitles',       # Filename for the subtitle file
        'format': 'bestaudio/best'    # Select the best available quality
    }

    # Using yt-dlp to extract information
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url, download=False)  # Only download info, not the video

        # Check if subtitles are available
        subtitles = result.get('requested_subtitles')
        subtitle_content = None
        if subtitles:
            language = list(subtitles.keys())[0]
            subtitle_url = subtitles[language]['url']
            subtitle_content = ydl.urlopen(subtitle_url).read().decode('utf-8')

        # Compile data
        video_data = {
            'title': result.get('title'),
            'description': result.get('description'),
            'url': result.get('webpage_url'),
            'subtitles': subtitle_content
        }
        
        return video_data


def extract_and_concat_subtitle_text(subtitle_text):
    # Regex to find all occurrences of text within <c>...</c> tags
    pattern = re.compile(r'<c>(.*?)<\/c>')
    matches = pattern.findall(subtitle_text)
    
    # Joining all the matched texts with a space
    concatenated_text = ''.join(matches)
    return concatenated_text

def extract_title(text):
    # Regex pattern to find text between 'title': ' and ', 'description
    pattern = re.compile(r"'title':\s*'([^']*)',\s*'description")
    
    # Searching the text for the pattern
    match = pattern.search(text)
    
    # If a match is found, return the captured group, otherwise return None
    return match.group(1) if match else None
    
    
    
def extract_description(input_string):
    # Regular expression to find text between ', 'description and ', 'url
    pattern = re.compile(r", 'description': '(.*?)', 'url'")
    match = pattern.search(input_string)
    
    # If a match is found, return the matched text; otherwise, return None
    if match:
        return match.group(1)
    else:
        return None
        
        
                
    

def find_first_youtube_url(text):
    # Pattern to match different YouTube URL formats
    pattern = re.compile(
        r'(https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+'
        r'|https?://youtu\.be/[\w-]+'
        r'|https?://(?:www\.)?youtube\.com/embed/[\w-]+'
        r'|https?://(?:www\.)?youtube\.com/channel/[\w-]+'
        r'|https?://(?:www\.)?youtube\.com/user/[\w-]+'
        r'|https?://music\.youtube\.com/watch\?v=[\w-]+'
        r'|https?://tv\.youtube\.com)'
    )
    
    # Search for the first YouTube URL in the text
    match = pattern.search(text)
    if match:
        return match.group(0)  # Return the matched URL
    return None  # If no URL is found, return None
'''
# Example usage
example_text = "Check out this video at https://www.youtube.com/watch?v=dQw4w9WgXcQ and this one at https://youtu.be/NpEaa2P7qZI"
first_youtube_url = find_first_youtube_url(example_text)
print(first_youtube_url)

# Example of using the function
video_url = 'https://www.youtube.com/watch?v=o27GDttmHxY'
video_info = download_youtube_video_info(video_url)
print(video_info)
text= extract_and_concat_subtitle_text(str(video_info))
print(text)

'''

## Thing to download all content from someone's JustFor.Fans NOW FIXED (hopefully)

### Written in Python 3.8 AND re-written and tested in python 3.11.5

1. Install requirements: `pip install -r requirements.txt`
1.1. Install ffmpeg and yt-dlp if you don;t have them in your system already
2. Set configuration
    1. `overwrite_existing` - will skip download if file exists
    2. `save_path` - destination folder - will save to same location as script folder if none provided
    3. `save_full_text` - will save text file with full description
    4. `file_name_format` - filename format, following values are available:
        * `name`
        * `post_date`
        * `post_id`
        * `desc`
2. Get UserID and UserHash values
    1.  Log into your JustFor.Fans account
    2.  Select performer's page
    3.  (in Chrome), hit F12 to open dev-console
    4.  Refresh page to view network activity
    5.  Locate `getPost.php` call, extract `UserID` and `UserHash4` values (in yellow)
    6.  Pass in as params when running script
        * `python app.py [UserID] [UserHash]`

![image](https://user-images.githubusercontent.com/12958294/115130004-859a5580-9fa0-11eb-9275-235d4ec51967.png)

## NOTE: This is a really ghetto implementation of a quickfix to make this abandoned project "just work" maybe i'll write it better in the future maybe not... idk ENJOY!

import unittest
import albumCheck
from unittest.mock import patch, mock_open

# your function import here
from albumCheck import process_artist_albums, is_music_file

class TestProcessArtistAlbums(unittest.TestCase):
    @patch('os.path.join')
    @patch('os.path.abspath')
    @patch('os.path.isdir')
    @patch('os.listdir')
    @patch('albumCheck.is_music_file')
    def test_artist_with_albums(self, mock_is_music_file, mock_listdir, mock_isdir, mock_abspath, mock_join):
        

           # Mock the join function to concatenate paths correctly
        
        mock_abspath.side_effect = lambda path: f'/abs{path.replace("/abs","")}'

        # Mock the join function to simply concatenate paths with "/"
        mock_join.side_effect = lambda *args: "/".join(args)
        
        # Mock the directory checks
        mock_isdir.side_effect = lambda path: {
            '/abs/music/artist': True,  # Artist directory exists
            '/abs/music/artist/album1': True,  # album1 directory exists
            '/abs/music/artist/album2': True,  # album2 directory exists
        }.get(path, False)
        
        # Mock the listdir function
        mock_listdir.side_effect = lambda path: {
            '/abs/music/artist': ['album1', 'album2'],  # Artist has 2 albums
            '/abs/music/artist/album1': ['song1.mp3', 'song2.mp3'],  # album1 has 2 songs
            '/abs/music/artist/album2': ['song3.mp3', 'song4.mp3', 'nonmusic.txt'],  # album2 has 2 songs and 1 non-music file
        }.get(path, [])
        
        
       
        # Mock the is_music_file function
        mock_is_music_file.side_effect = lambda path: path.endswith('.mp3')

        # Run the function
        result = process_artist_albums('/music', 'artist')

        print("Result Dictionary:", result)
      
        
        # Verify that '/abs/music/artist' was checked with os.path.isdir
        mock_isdir.assert_any_call('/abs/music/artist')
        
        # Verify that '/abs/music/artist' was listed with os.listdir
        mock_listdir.assert_any_call('/abs/music/artist')

        # Print out all calls to the mocks for further inspection
        print("isdir calls:", mock_isdir.call_args_list)
        print("listdir calls:", mock_listdir.call_args_list)
       

        # Assertions
        self.assertIn('artist;album1', result)  # Check if 'artist;album1' is in the result
        self.assertIn('artist;album2', result)  # Check if 'artist;album2' is in the result
        self.assertEqual(result['artist;album1'], 2)  # Ensure album1 has 2 songs
        self.assertEqual(result['artist;album2'], 2)  # Ensure album2 has 2 songs


    @patch('os.path.join')
    @patch('os.path.abspath')
    @patch('os.path.isdir')
    def test_artist_directory_not_exists(self, mock_isdir, mock_abspath, mock_join):
         # Mock the abspath function
        mock_abspath.side_effect = lambda path: f'/abs{path}'
        
        # Mock the join function
        mock_join.side_effect = lambda *args: "/".join(args)

        # Mock the directory check
        mock_isdir.return_value = False

        # run the function
        Dictionary = process_artist_albums('/music', 'non_existing_artist')

        # ensure the dictionary is still empty since the artist doesn't exist
        self.assertEqual(Dictionary, {})
    
    # add more test cases as needed

if __name__ == '__main__':
    unittest.main()

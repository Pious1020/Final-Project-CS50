from final_project import get_channel_id, data_cleanup, play_video

def test_get_channel_id():
    assert get_channel_id("MKBHD") == "UCBJycsmduvYEL83R_U4JriQ"
    assert get_channel_id("Linus Tech Tips") == "UCXuqSBlHAE6Xw-yeJA0Tunw"
    assert get_channel_id("The Verge") == "UCddiUEpeqJcYeBxX1IVBKvQ"
    assert get_channel_id("Unbox Therapy") == "UCsTcErHg8oDvUnTzoqsYeNw"

def test_data_cleanup():
    assert data_cleanup({"items": [{"snippet": {"title": "Me at the zoo", "publishedAt": "2005-04-24T03:31:52Z"}, "id": {"videoId": "jNQXAC9IVRw"}}]}) == [{"title": "Me at the zoo", "url": "https://www.youtube.com/watch?v=jNQXAC9IVRw", "date": "2005-04-24T03:31:52Z"}]

def test_play_video():
    result = play_video("https://www.youtube.com/watch?v=jNQXAC9IVRw")

    assert result == None

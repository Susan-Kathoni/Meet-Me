from django.test import TestCase

# Create your tests here.
class ProfileTestClass(TestCase):
    #Set up method

    def setUp(self):
        self.new_user = User(username='Padus', email='paduspadus465.com', password='Padus1')
        self.new_user.save()
        self.new_profile = Profile(user=self.new_user,profile_picture="image.jpeg",bio="just testing", contact='paduspadus465.com')
    
    # Testing  instance
    def test_instance(self):
        self.assertTrue(isinstance(self.new_profile,Profile))
    
    def test_save_method(self):
        self.new_profile.save_profile()
        profile = Profile.objects.all()
        self.assertTrue(len(profile)>0)

    def test_delete_method(self):
        self.new_profile.save_profile()
        self.new_profile.delete_profile()
        profile = Profile.objects.all()
        self.assertTrue(len(profile)==0) 
        
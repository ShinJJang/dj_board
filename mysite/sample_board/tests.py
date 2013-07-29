import unittest
from mock import Mock

class Test(unittest.TestCase):
    
    def ModelCreate(self):
        from .models import DjangoBoard
        board = DjangoBoard(subject = 'ef',
                name = 'ef',
                mail = 'ef',
                memo = 'ef',
                created_date = timezone.now(),
                hits = 0,
                likes = 0
                )
        
        
        
    def formvalid(self):
        from .forms import UploadFileForm
        
        
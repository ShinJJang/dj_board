# Create your views here.
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.utils import timezone
from sample_board.models import DjangoBoard
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from sample_board.pagingHelper import pagingHelper

#한글!!
rowsPerPage = 2

def home(request):
	boardList = DjangoBoard.objects.order_by('-id')[0:2]
	current_page = 1

	# model을 사용해서 전체 데이터 갯수를 구한다.
	totalCnt = DjangoBoard.objects.all().count()

	# 이것은 페이징 처리를 위해 생성한 간단한 헬퍼 클래스이다.
	pagingHelperIns = pagingHelper();
	totalPageList = pagingHelperIns.getTotalPageList(totalCnt, rowsPerPage)
	print 'totalPageList', totalPageList

	return render_to_response('listSpecificPage.html', {'boardList':boardList, 'totalCnt':totalCnt,
								'current_page':current_page, 'totalPageList':totalPageList})


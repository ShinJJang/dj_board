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
	boardList = DjangoBoard.objects.order_by('-id')[0:rowsPerPage]
	current_page = 1

	# model을 사용해서 전체 데이터 갯수를 구한다.
	totalCnt = DjangoBoard.objects.all().count()

	# 이것은 페이징 처리를 위해 생성한 간단한 헬퍼 클래스이다.
	pagingHelperIns = pagingHelper();
	totalPageList = pagingHelperIns.getTotalPageList(totalCnt, rowsPerPage)
	print 'totalPageList', totalPageList

	return render_to_response('listSpecificPage.html', {'boardList':boardList, 'totalCnt':totalCnt,
								'current_page':current_page, 'totalPageList':totalPageList})

def show_write_form(request):
	return render_to_response('writeBoard.html')

@csrf_exempt
def DoWriteBoard(request):
	br = DjangoBoard (subject = request.POST['subject'],
				name = request.POST['name'],
				mail = request.POST['email'],
				memo = request.POST['memo'],
				created_date = timezone.now(),
				hits = 0,
				likes = 0
				)
	br.save()

	# 저장을 했으니, 다시 조회해서 보여준다.
	url = '/listSpecificPageWork?current_page=1'
	return HttpResponseRedirect(url)


def listSpecificPageWork(request):
	current_page = request.GET['current_page']
	totalCnt = DjangoBoard.objects.all().count()

	print 'current_page=', current_page

	# 페이지를 가지고 범위 데이터를 조사한다 -> raw SQL 사용함
	#boardList = DjangoBoard.objects.raw('SELECT Z.* FROM(SELECT X.*, ceil( rownum / %s ) as page FROM ( SELECT ID, SUBJECT, NAME, CREATED_DATE, MAIL, MEMO, HITS, LIKES \
	 #FROM SAMPLE_BOARD_DJANGOBOARD ORDER BY ID DESC) X ) Z WHERE page = %s',[rowsPerPage, current_page])
	PageIndex = int(current_page)-1
	start = int(rowsPerPage*PageIndex)
	boardList = DjangoBoard.objects.raw('SELECT * FROM SAMPLE_BOARD_DJANGOBOARD ORDER BY ID DESC LIMIT %s, %s', [start, rowsPerPage])
        
	 
	print 'boardList=', boardList, 'count()=', totalCnt

	# 전체 페이지를 구해서 전달
	pagingHelperIns = pagingHelper();
	totalPageList = pagingHelperIns.getTotalPageList(totalCnt, rowsPerPage)

	print 'totalPageList', totalPageList

	return render_to_response('listSpecificPage.html', {'boardList':boardList, 'totalCnt':totalCnt,
								'current_page':int(current_page), 'totalPageList':totalPageList})
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.utils import timezone
from sample_board.models import DjangoBoard
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from sample_board.pagingHelper import pagingHelper
from .forms import UploadFileForm

#한글!!
rowsPerPage = 3

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
	# Handle file upload
	if request.method == 'POST' :
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid() :
			br = DjangoBoard (subject = request.POST['subject'],
				name = request.POST['name'],
				mail = request.POST['mail'],
				memo = request.POST['memo'],
				created_date = timezone.now(),
				hits = 0,
				likes = 0
				)
			if request.FILES.get('file_1'):
				file_1 = request.FILES['file_1']
				
			if request.FILES.get('file_2'):
				file_2 = request.FILES['file_2']
			br.save()

			# Redirect to the board list after POST
			url = '/listSpecificPageWork?current_page=1'
			return HttpResponseRedirect(url)
		else :
			form = UploadFileForm # A empty, unbound form
	
	return redirect('/fail/')


def listSpecificPageWork(request):
	current_page = request.GET['current_page']
	totalCnt = DjangoBoard.objects.all().count()

	print 'current_page=', current_page

	# 페이지를 가지고 범위 데이터를 조사한다 -> raw SQL 사용함
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

def viewWork(request):
	pk = request.GET['memo_id']
	boardData = DjangoBoard.objects.get(id=pk)

	# 조회수를 늘린다
	DjangoBoard.objects.filter(id=pk).update(hits = boardData.hits + 1)

	return render_to_response('viewMemo.html',{'memo_id': request.GET['memo_id'],
								'current_page': request.GET['current_page'],
								'searchStr': request.GET['searchStr'],
								'boardData': boardData})

def listSearchedSpecificPageWork(request):
	searchStr = request.GET['searchStr']
	pageForView = request.GET['pageForView']

	totalCnt = DjangoBoard.objects.filter(subject__contains=searchStr).count()

	pagingHelperIns = pagingHelper();
	totalPageList = pagingHelperIns.getTotalPageList(totalCnt, rowsPerPage)

	PageIndex = int(pageForView)-1
	start = int(rowsPerPage*PageIndex)

	boardList = DjangoBoard.objects.raw('SELECT X.* FROM ( SELECT * FROM SAMPLE_BOARD_DJANGOBOARD WHERE SUBJECT LIKE %s) X ORDER BY ID DESC LIMIT %s, %s', [searchStr, start, rowsPerPage])

	return render_to_response('listSearchedSpecificPage.html', {'boardList': boardList, 'totalCnt': totalCnt,
								'pageForView': int(pageForView), 'searchStr': searchStr, 'totalPageList': totalPageList})

def listSpecificPageWork_to_update(request):
	memo_id = request.GET['memo_id']
	#current_page = request.GET['current_page']
	#searchStr = request.GET['searchStr']
	boardData = DjangoBoard.objects.get(id=memo_id)
	return render_to_response('viewForUpdate.html', {'memo_id':request.GET['memo_id'],
								'current_page':request.GET['current_page'],
								'searchStr':request.GET['searchStr'],
								'boardData':boardData})

@csrf_exempt
def updateBoard(request):
	memo_id = request.POST['memo_id']
	current_page = request.POST['current_page']
	searchStr = request.POST['searchStr']
	
	br = DjangoBoard.objects.get(id=memo_id)
	br.mail = request.POST['mail']
	br.subject = request.POST['subject']
	br.memo = request.POST['memo']

	if request.FILES.get('file_1'):	
		br.file_1 = request.FILES['file_1']

	if request.FILES.get('file_2'):	
		br.file_2 = request.FILES['file_2']

	br.save()

	# Display Page => POST 요청은 redirection으로 처리
	url = '/listSpecificPageWork?current_page=' + str(current_page)
	return HttpResponseRedirect(url)


def DeleteSpecificRow(request):
	memo_id = request.GET['memo_id']
	current_page = request.GET['current_page']

	p = DjangoBoard.objects.get(id=memo_id)
	p.delete()

	# 마지막 메모를 삭제하는 경우, 페이지를 하나 줄임
	totalCnt = DjangoBoard.objects.all().count()
	pagingHelperIns = pagingHelper();

	totalPageList = pagingHelperIns.getTotalPageList(totalCnt, rowsPerPage)
	print 'totalPages', totalPageList

	if(int(current_page) in totalPageList):
		print 'current_page No Change'
		current_page = current_page
	else:
		current_page = int(current_page) - 1
		print 'current_page--'

	url = '/listSpecificPageWork?current_page=' + str(current_page)
	return HttpResponseRedirect(url)

@csrf_exempt
def searchWithSubject(request):
	searchStr = request.POST['searchStr']
	print 'searchStr', searchStr

	url = '/listSearchedSpecificPageWork?searchStr=' + searchStr + '&pageForView=1'
	return HttpResponseRedirect(url)

@csrf_exempt
def rowmodify(request):
	rowsPerPage = request.POST['rowsPerPage']

	url = '/listSpecificPageWork?current_page=' + str(rowsPerPage)
	return HttpResponseRedirect(url)

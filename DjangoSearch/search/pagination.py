from django.http import QueryDict
class Pagination:
	def __init__(self, page_num, all_count,per_num=10):
		"""
		:param page_num:  当前的页码数
		:param all_count: 总数据量
		:param per_num:   每页显示的数据条数
		:param self.total_page_num:  总页码数
		:param self.page_start:  起始页码数
		:param self.page_end:    终止页码数
		"""
		try:
			page_num = int(page_num)
			if page_num <= 0:
				page_num = 1
		except Exception as e:
			page_num = 1
		self.page_num = page_num
		self.all_count = all_count
		self.per_num = per_num
		total_page_num, more = divmod(all_count, per_num)
		if more:
			total_page_num += 1
		if total_page_num > 6 and page_num >= 4 and page_num < total_page_num-2:
			page_start=page_num-3
			page_end=page_num+2
		elif total_page_num > 6 and page_num < 4:
			page_start = 1
			page_end = 6
		elif  total_page_num <= 6:
			page_start = 1
			page_end = total_page_num
		else:
			page_start = total_page_num-5
			page_end = total_page_num
		self.page_start = page_start
		self.page_end = page_end
		self.total_page_num = total_page_num
	@property
	def start(self):
		return (self.page_num - 1) * self.per_num

	@property
	def end(self):
		return self.page_num * self.per_num

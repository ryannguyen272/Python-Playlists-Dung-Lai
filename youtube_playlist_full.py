"""
Bài hoàn thiện nốt các yêu cầu mở rộng theo khóa học của Dũng Lại - Khóa Python cơ bản
1 - Thêm nút bấm chuyển Playlist
2 - Thêm chú thích di chuyển theo con trỏ chuột khi di chuột vào dòng video tương ứng
3 - Hiển thị đánh giá (Rating) bằng sao và mô tả (Description) trên nhiều dòng của từng Playlist
4 - Xử lý vấn đề số lượng Video quá nhiều bằng cách cắt trang
5 - Xử lý vấn đề phát sinh nếu tên (title) của video quá dài >40 ký tự thì cắt bớt và thêm "..."
6 - Đổi màu các video đã ấn mở
7 - Chèn ảnh cho từng Playlist: mục này vì mình lười rồi nên các bạn tự nghiên cứu nốt, mình để trống cái ô vuông màu vàng để chèn ảnh (phương án gợi ý: thêm 1 self.img_playlist vào class Playlist, thêm link hình ảnh vào từng playlist trong file data.txt, rồi gọi ra với list tương ứng)
Ryan - 
"""

#truyền module
import pygame, sys
import webbrowser

#định nghĩa thành phần của video
class Video:
	def __init__(self, title, link):#định nghĩa các thành phần trong 1 video
		self.title = title			#tiêu đề video
		self.link = link			#link của video
		self.seen = False			#cờ hiệu thể hiện chưa xem

	def open(self):					#Hàm mở video
		webbrowser.open(self.link)	#mở link bằng trình duyệt web
		print("Open", self.title)	#in ra cmd: đã mở tiêu đề video nào
		self.seen = True			#chuyển giá trị cờ hiệu thành đã xem
#định nghĩa thành phần của playlist		
class Playlist:						
	def __init__(self, name, description, rating, videos):#định nghĩa các thành phần trong 1 playlist
		self.name = name				#tên playlist
		self.description = description	#mô tả của playlist
		self.rating = rating			#thang điểm đánh giá playlist (max 5)
		self.videos = videos			#danh sách video trong 1 playlist
#định nghĩa thành phần của 1 nút bấm
class TextButton:						
	def __init__(self, text, position):
		self.text = text					#nội dung nút bấm
		self.position = position			#điểm bắt đầu của nút bấm, dạng tạo độ (x,y)

	def is_mouse_on_text(self):				#Hàm xác định con trỏ chuột có đang nằm trên nút bấm
		mouse_x, mouse_y = pygame.mouse.get_pos()	#lấy tọa độ con trỏ chuột hiện tại
		if (self.position[0] < mouse_x < self.position[0] + self.text_box[2]) and (self.position[1] < mouse_y < self.position[1] + self.text_box[3]): #xác định con trỏ chuột có nằm trong vùng tọa độ của nút bấm
			return True						#Trả về giá trị Có
		return False						#Trả về giá trị Không

	def draw(self, DISPLAY, seen=False):	#Hàm vẽ ra nút bấm và hiệu ứng cho nút, xác định nút đã từng bấm hay chưa (mặc định là chưa False)
		font = pygame.font.SysFont("sans", 20)					#định dạng loại font và kích cỡ chữ
		if len(self.text) > 40:									#nếu độ dài chữ dài hơn 40 kỹ tự
			s_text = self.text[0:36] + "..."					#gán tạm 1 chuỗi có tiêu đề cắt đi còn 37 kỹ tự và thêm "..." (37 vì tính cả vị trí [0])
		else:
			s_text = self.text									#nếu tiêu đề không dài quá 40 ký tự thì gán cả tiêu đề cho chuỗi tạm (s_text)
		text_render = font.render(s_text, True, (0,0,0))	 	#truyền vào dạng font, nội dung, độ sắc nét, màu sắc chữ (màu đen) - bước này không có nhiều ý nghĩa, chỉ để chống lỗi trong 1 số trường hợp, các dòng lệnh sau sẽ thay đổi giá trị của dòng này
		self.text_box = text_render.get_rect()					#thông số hình chữ nhật bao quanh chữ (hình chữ nhật này không hiện trên màn hình, chỉ ở dạng tọa độ)
		if self.is_mouse_on_text():								#nếu trỏ chuột đang nằm trong hình chữ nhật bao quanh chữ
			text_render = font.render("♪ " + s_text, True, (0,0,255))	#truyền vào dạng font, nội dung, thêm ký ♪ vào đầu chuỗi khi di trỏ chuột tới chuỗi, tăng độ nét, màu sắc chữ (xanh blue)
			pygame.draw.line(DISPLAY, (0,0,255), (self.position[0]-1, self.position[1] + self.text_box[3]), (self.position[0] + self.text_box[2] + 16, self.position[1] + self.text_box[3]),3) #vẽ 1 đường kẻ dựa vào tọa độ của hình chữ nhật bao quanh chữ (điểm đầu, điểm cuối)
		else:
			if seen:		#nếu giá trị đã xem của video là đúng
				text_render = font.render(s_text, True, (128,0,0))	#in chuỗi lên màn hình tương tự như trên nhưng thay bằng màu tím (thể hiện đã xem)
			else:
				text_render = font.render(s_text, True, (0,0,0))	#in chuỗi lên màn hình tương với màu đen (thể hiện chưa xem)
		DISPLAY.blit(text_render, self.position)					#Bắt đầu vẽ ra màn hình DISPLAY với các thông số bên trên, tọa độ bắt đầu vẽ (position sẽ được truyền từ định nghĩa của nút bấm, tức là có sẵn)
	
	#Hàm vẽ ghi chú
	def draw_info(self, DISPLAY):								#Hàm vẽ phần ghi chú đi theo con trỏ chuột
		font = pygame.font.SysFont("sans", 15)					#định dạng loại font và kích cỡ chữ
		text_render = font.render(self.text, True, (65,65,65))	#truyền vào nội dung, độ sắc nét, màu ghi xám
		self.text_box_info = text_render.get_rect()				#xác định thông số hình chữ nhật bao quanh chuỗi
		pygame.draw.rect(DISPLAY, (255,255,167), (self.position[0]-10, self.position[1]-5, self.text_box_info[2]+20, self.text_box_info[3]+10),0,5) #vẽ 1 hình chữ nhật đặc bên trong (0), màu vàng nhạt bo góc tròn (độ bo cong = 5)
		DISPLAY.blit(text_render, self.position)				#Bắt đầu vẽ ra màn hình DISPLAY với các thông số bên trên
#Hàm đọc 1 video đơn lẻ từ file
def read_video_from_txt(file):			#không dùng lệnh mở đọc file vì lệnh này sẽ dùng ở hàm khác để mở và ta sẽ gọi hàm này ra sau
	title = file.readline().rstrip()	#lấy giá trị tiêu đề trong 1 dòng có trên file và hủy bỏ đi giá trị xuống dòng ở cuối
	link = file.readline().rstrip()		#lấy giá trị link trong 1 dòng có trên file và hủy bỏ đi giá trị xuống dòng ở cuối
	video = Video(title, link)			#tập hợp tiêu đề và link thành 1 kiểu video đã được định nghĩa tại class Video
	return video						#trả về giá trị video (sau này dùng để in ra hoặc gán)
#Hàm đọc và tổng hợp tập hợp videos trong cùng 1 playlist từ file
def read_videos_from_txt(file):			#không dùng lệnh mở đọc file vì lệnh này sẽ dùng ở hàm khác để mở và ta sẽ gọi hàm này ra sau
	videos = []							#khởi tạo 1 tập hợp các video là videos (kiểu list)
	total = file.readline()				#lấy giá trị số lượng video có trong 1 playlist dựa vào dòng này trong file (nó sẽ được ke đúng dòng cần lấy dựa vào thứ tự nó được gọi sau này ở hàm khác)
	for i in range(int(total)):			#cho giá trị i chạy đến hết tổng số video
		video = read_video_from_txt(file)	#gọi hàm để lấy giá trị (title, link) trong file gán cho 1 video. ở đây ta không dùng đến i vì mỗi lần đọc lệnh sẽ gọi 1 dòng tiếp theo trong file
		videos.append(video)			#gán video mới tổng hợp được vào cuối của tập hợp videos đến khi hết vòng lặp for
	return videos						#trả về giá trị tập hợp videos dùng để in hoặc gán sau này
#Hàm đọc 1 playlist đơn lẻ từ file
def read_playlist_from_txt(file):		#không dùng lệnh mở đọc file vì lệnh này sẽ dùng ở hàm khác để mở và ta sẽ gọi hàm này ra sau
	playlist_name = file.readline().rstrip()			#lấy giá trị tên (name) của list từ 1 dòng trong file, hủy đi ký tự xuống dòng ở cuối
	playlist_description = file.readline().rstrip()		#lấy giá trị mô tả (description) của list từ 1 dòng trong file, hủy đi ký tự xuống dòng ở cuối
	playlist_rating = file.readline().rstrip()			#lấy giá trị đánh giá (rating) của list từ 1 dòng trong file, hủy đi ký tự xuống dòng ở cuối
	playlist_videos = read_videos_from_txt(file)		#gọi Hàm tổng hợp videos trong cùng 1 playlist để lấy ra videos trong playlist đó
	playlist = Playlist(playlist_name,playlist_description,playlist_rating,playlist_videos) #Tổng hợp tất cả các thành phần lấy được để tạo ra 1 Playlist đầy đủ như đã định nghĩa tại Class Playlist ở trên
	return playlist						#trả về giá trị 1 playlist để in hoặc gán sau này
#Hàm đọc 1 tập hợp tổng thể các playlist có trong file
def read_playlists_from_txt():			#Hàm này sẽ dùng để gọi tất cả các hàm đọc file phía trên vào bên trong nó và nó sẽ có nhiệm vụ phải Mở chức năng đọc file lên cho cả nhóm
	playlists = []						#tạo 1 tập hợp playlists rỗng để sau này chứa tất cả các playlist
	with open("data.txt", "r") as file:	#mở file data.txt với chế độ chỉ đọc 'r'
		total = file.readline()			#đọc dòng đầu tiên trong file để lấy tổng số playlist có trong file, giá trị này phải đc ghi trong file từ trước đó
		for i in range(int(total)):		#cho giá trị i chạy từ 0 đến hết tổng số file (không bao gồm số tổng số file nhé đây là luật của vòng for)
			playlist = read_playlist_from_txt(file)	#gọi Hàm để lấy tất cả thông tin của cả 1 playlist có trong file
			playlists.append(playlist)	#gán playlist vừa lấy được ghi vào cuối tập hợp tổng hợp playlists
	return playlists					#trả về giá trị tập hợp playlists để in hoặc gán sau này
#Hàm xác định con trỏ chuột có nằm trong vùng tạo độ xác định bởi x1, y1, x2, y2 được truyền vào
def is_mouse_on_btn(x1,y1,x2,y2):
		mouse_x, mouse_y = pygame.mouse.get_pos()		#lấy tọa độ con trỏ chuột hiện tại
		if (x1 < mouse_x < x2) and (y1 < mouse_y < y2):	#nếu nằm trong vùng đã xác định
			return True									#trả về đúng True
		return False									#trả về sai False
#Hàm để tách từng từ trong chuỗi, sau đó in vào 1 khoanh vùng nhất định
#Lý do có hàm này là trong Pygame không thể dùng các lệnh in thông thường xử lý chuỗi như print, và cũng không nhận các ký tự xuống dòng như \n,...
def blit_text(surface, text, pos, font, color=pygame.Color('black')): #pygame.Color() lấy màu đã được định nghĩa sẵn trong module Pygame mà không cần dùng bảng màu RGB
    words = [word.split(' ') for word in text.splitlines()]  #Lưu ý: words ở đây giống như 1 kiểu list lồng list [[],[].[]], mỗi phần tử của list words là 1 đoạn text (dạng list), mỗi phần tử của đoạn text này chứa 1 từ được cắt chuỗi 1 text, văn bản có thể có nhiều chuỗi text (dùng my_text.splitlines() để cắt ra đoạn text khác nhau dựa vào kí tự '\' cuối đoạn và split() để cắt từng từ ra dựa vào dấu cách sau mỗi từ). Hàm này dùng cho nhiều trường hợp khác nhau, nếu như phần text dài và nhiều phần vẫn có thể xử lý được, dùng cho bài tập này thì hơi thừa khả năng
    space = font.size(' ')[0]  #định nghĩa 1 khoảng trắng để sau này vẽ thêm vào sau mỗi từ
    max_width, max_height = (200, 200)	#độ rộng và dài của vùng giới hạn sẽ vẽ chữ
    x, y = pos							#tọa độ bắt đầu của vùng giới hạn sẽ vẽ chữ
    for line in words:					#chạy từng list dòng (line) trong list  văn bản (words)
        for word in line:				#chạy từng từ (word) trong list dòng (line)
            word_surface = font.render(word, True, color)		#tạo nội dung, độ sắc nét, màu sắc để chuẩn bị in từ (word) ra màn hình
            word_width, word_height = word_surface.get_size()	#xác định độ rộng và chiều cao của từ (word) đó
            if x + word_width >= max_width:						#nếu tạo độ bắt đầu của vùng vẽ + độ rộng của từ lớn hơn hoặc bằng độ rộng vùng giới hạn thì sẽ xuống dòng
                x = pos[0]  									#xuống dòng mới cần reset lại tọa độ x về ban đầu của vùng giới hạn (về đầu dòng)
                y += word_height								#đồng thời xuống 1 dòng mới bằng cách cộng thêm 1 lần chiều cao của 1 từ
            surface.blit(word_surface, (x, y))					#Vẽ từ đó theo tạo độ bắt đầu x,y
            x += word_width + space								#sau khi vẽ, tăng tọa độ của từ tiếp theo lên 1 khoảng bằng độ rộng của từ trước đó + 1 khoảng trắng (space) đã được định nghĩa ở trên để tính tọa độ bắt đầu của từ tiếp theo
        x = pos[0]												#đã vẽ hết 1 dòng (line) cần xuống dòng mới bất kể còn chỗ trống hay không. Cần reset lại tọa độ x về ban đầu của vùng giới hạn (về đầu dòng)
        y += word_height										#đồng thời xuống 1 dòng mới bằng cách cộng thêm 1 lần chiều cao của 1 từ
#Hàm chính (main)
def main():
	#khai báo khởi tạo 1 số biến ban đầu
	pygame.init()	#khởi tọa giá trị init pygame
	DISPLAY = pygame.display.set_mode((600, 400), pygame.RESIZABLE) #tạo thông số cho bề mặt hiển thị với giá trị 600x400 pixel, loại có thể dùng chuột thay đổi kích thước RESIZABLE (nếu không có giá trị này vùng hiển thị sẽ khóa cứng kích cỡ)
	pygame.display.set_caption('Youtube Player')	#tiêu đề cho vùng hiển thị
	running = True			#tạo 1 biến với giá trị True để gán vào while tạo vòng lặp vô hạn, hiển thị các nôi dung của chương trình
	clock = pygame.time.Clock()	#khởi tạo clock để truyền nhịp làm mới vùng hiển thị
	RED = (255,0,0)	#tạo màu đỏ theo mã RGB # COLOR = (255,0,255)	#tạo 1 màu theo mã RGB

	playlists = read_playlists_from_txt()	#nạp file dữ liệu
	playlists_btn_list = []					#tạo 1 list chứa nút bấm các playlist
	videos_btn_list = []					#tạo 1 list chưa nút bấm các video
	margin = 50								#khoảng cách 50 pixel cho mỗi video hiển thị ra
	# row_playlist = 1	#số playlist sẽ hiển thị
	row_video = 6							#số video tối đa trong 1 trang playlist có thể được hiển thị, phần video lớn hơn sẽ sang trang sau
	len_playlists = len(playlists)			#số tổng số playlist có trong dữ liệu
	len_videos = 1							#khởi tạo biến chứa số trang hiển thị video trong 1 list (luôn tối thiểu là 1)
	now_playlist = 1						#khởi tạo biến chứa thứ tự playlist đang làm việc
	now_videopage = 1						#khởi tạo biến chứa thứ tự trang video đang làm việc (1 trang có row_video được hiển thị)
	
	while running:			#vòng lặp vô hạn để hiển thị chương trình, luôn trả về True
		clock.tick(60)		#Vẽ lại màn hình 60 nhịp trong 1 giây
		DISPLAY.fill((255, 255, 255))	#màu nền của toàn bộ phần hiển thị là màu trắng
		#vẽ các vị trí nút chức năng
		pygame.draw.rect(DISPLAY, (255,255,0), (50,200,120,120),0,10)  			#Đây là khu vực hình chữ nhật để dành chèn ảnh cho Playlist 
		pygame.draw.polygon(DISPLAY, RED, ((35, 45), (55, 45), (45, 25)))		#nút tiến playlist
		pygame.draw.polygon(DISPLAY, RED, ((35, 75), (55, 75), (45, 95)))		#nút lùi playlist
		pygame.draw.line(DISPLAY, RED, (220, 50), (220, 330), 3)				#Dòng kẻ ngăn cách playlist videos
		pygame.draw.polygon(DISPLAY, RED, ((240, 45), (260, 45), (250, 25)))	#nút tiến trang videos
		pygame.draw.polygon(DISPLAY, RED, ((240, 75), (260, 75), (250, 95)))	#nút lùi trang videos
		#vẽ số thứ tự đang làm việc của playlists và videos
		font = pygame.font.SysFont("sans", 20)													#truyền giá trị kiểu chữ, cỡ chữ 20
		text_render = font.render(str(now_playlist)+"/"+str(len_playlists), True, (0,0,0))		#truyền nội dung hiển thị số playlist đang làm việc trên tổng số playlists hiện có
		DISPLAY.blit(text_render, (33,48))														#vẽ nội dung ra màn hình
		text_render = font.render(str(now_videopage)+"/"+str(len_videos), True, (0,0,0))		#truyền nội dung hiển thị số trang videos đang làm việc trên tổng số trang videos hiện có
		DISPLAY.blit(text_render, (238,48))														#vẽ nội dung ra màn hình

		img = pygame.image.load('star_rating.jpg')					#nạp hình ảnh ngôi sao để hiển thị trong phần đánh giá (rate) của playlist
		for i in range(int(playlists[now_playlist-1].rating)):		#vòng lặp cho i chạy đến hết số đánh giá (rating) của playlist đang làm việc
			DISPLAY.blit(img,(110+i*10,79))							#mỗi 1 vòng lặp, sẽ in ra ảnh ngôi sao ở trên và dịch sang phải 10 pixel so với ngôi sao trước đó. bắt đầu vẽ từ tọa độ (110,79)
		font = pygame.font.SysFont("sans", 15)						#truyền giá trị kiểu chữ, cỡ chữ 15
		text_render = font.render("Description: ", True, (0,0,0))	#truyền nội dung để vẽ từ Description:
		DISPLAY.blit(text_render, (20,105))							#vẽ nội dung ra màn hình
		text_desc = playlists[now_playlist-1].description			#lấy nội dùng phần mô tả (description) của playlist đang làm việc
		blit_text(DISPLAY,text_desc,(20,130),font)					#vẽ nội dung phần mô tả ra màn hình bằng Hàm blit_text đã được định nghĩa ở trên (vì description thường là 1 văn bản dài cần phải sử lý trước khi vẽ ra)
		font = pygame.font.SysFont("sans", 20)						#truyền giá trị kiểu chữ, cỡ chữ 20
		text_render = font.render("rate: ", True, (0,0,0))			#truyền nội dung để vẽ từ rate:
		DISPLAY.blit(text_render, (70,70))							#vẽ nội dung ra màn hình
		#Vẽ tên playlist đang làm việc ra màn hình tại tọa độ (70,50)
		text_render = font.render(playlists[now_playlist-1].name, True, (0,0,0))
		DISPLAY.blit(text_render, (70,50))
		#Vẽ tiêu đề (title) các video được hiển thị tại trang đang làm việc
		playlist = playlists[now_playlist-1]			#Lấy giá trị playlist đang làm việc
		videos_btn_list = []							#làm mới lại mảng lưu trữ nút bấm các videos
		for j in range(len(playlist.videos)):			#vòng lặp cho i chạy đến cuối danh sách videos có trong playlist đang làm việc
			video_btn = .//TextButton(str(j+1) + ". " + playlist.videos[j].title, (280, 50 + margin*(j%row_video))) #lấy thông tin (tên nút, tọa độ nút) của từng video có trong playlist đang làm việc. j chia row_video lấy dư để video sang trang mới được in lại từ trên xuống, nếu k có dòng này, vị trí video dù có sang trang các video vẫn bị in thấp dần xuống
			videos_btn_list.append(video_btn)			#thêm các thông tin các nút bấm video vào list danh sách nút bấm video
		#Tính toán tổng số trang của playlist đang làm việc
		len_videos = (len(videos_btn_list)-1)//row_video+1	#Tổng số trang sẽ bằng tổng số video/số video hiển thị trong 1 trang (row_video) rồi làm tròn lên (có thể dùng ceil() nhưng không muốn import math). Chỗ này nếu chia hết dư 0 mà lại công thêm 1 trang, thì trang mới sẽ bị trắng không có video nào. đề loại bỏ việc này thì trừ tổng số video đi 1 đơn vị.
		if len_videos == 0:									#trường hợp playlist không có video thì sẽ là -1 / row_video và theo tính toán trên sẽ ra 0, để không hiện tổng số trang là 0 thì nếu bằng 0 ta gán thành 1
			len_videos = 1
		#Vẽ ra danh sách video có trong playlist đang làm việc tại trang đang làm việc
		for i in range(len(videos_btn_list)):				#vòng lặp i chạy tới tổng số danh sách nút bấm video trong playlist. Sử dụng i lọc ra số thứ tự các nút bấm video sẽ hiện trong trong này (không gồm các nút video ở trang trước và sau nó)
			if ((now_videopage-1)*row_video) <= i < (row_video*now_videopage):	#Các video nằm trong vị trí i sẽ đủ điều kiện hiển thị khi: i lớn hơn hoặc bằng (số trang hiện tại -1)*số video hiện trong 1 trang (row_video), i nhỏ hơn số trang hiện tại * số trang hiện trong 1 trang (row_video)
				videos_btn_list[i].draw(DISPLAY, playlist.videos[i].seen)		#vẽ ra các nút video thỏa mãn điều khiện hiển thị, đống thời kiểm tra đã xem hay chưa (với giá trị seen) thông qua hàm draw() được định nghĩa ở trên
				if videos_btn_list[i].is_mouse_on_text():						#nếu con trỏ chuột nằm tại vị trí của nút video
					mouse_x, mouse_y = pygame.mouse.get_pos()					#lấy tọa độ của con trỏ chuột
					info_video = TextButton("url: " + playlist.videos[i].link, (mouse_x+20, mouse_y+25))	#hiện nội dung ghi chú của video chạy theo con trỏ chuột với hàm TextButton() được định nghĩa ở trên
					info_video.draw_info(DISPLAY)								#vẽ ra phần ghi chú thông tin
			#Các sự kiện diễn ra trong quá trình chạy chương trình
		for event in pygame.event.get():				#lấy sự kiện
			if event.type == pygame.MOUSEBUTTONDOWN:	#nếu sảy ra sự kiện nhấp chuột xuống (khác với nhả chuột ra MOUSEBUTTONUP)
				if event.button == 1:					#event.button = 1 là phát hiện ấn chuột trái (3 là chuột phải, 2 là chuột giữa, 4/5 là vê chuột lên/xuống)
					if is_mouse_on_btn(35,25,55,45):	#ấn chuột trái tại vị trái nút tiến playlist
						print("ấn tiến playlist")		#in ra cmd để kiểm tra
						now_playlist +=1				#tăng thứ tự playlist lên 1
						now_videopage = 1				#chuyển playlist thì phải đưa trang video về đầu
					if is_mouse_on_btn(35,75,55,95):	#ấn chuột trái tại vị trái nút lùi playlist
						print("ấn lùi playlist")		#in ra cmd để kiểm tra
						now_playlist -=1				#giảm thứ tự playlist xuống 1
						now_videopage = 1				#chuyển playlist thì phải đưa trang video về đầu
					if is_mouse_on_btn(240,25,260,45):	#ấn chuột trái tại vị trái nút tiến trang video
						print("ấn tiến trang video")	#in ra cmd để kiểm tra
						now_videopage +=1				#tăng số trang lên 1
					if is_mouse_on_btn(240,75,260,95):	#ấn chuột trái tại vị trái nút tiến trang video
						print("ấn lùi trang video")		#in ra cmd để kiểm tra
						now_videopage -=1				#giảm số trang xuống 1
					#xử lý khi tăng quá hoặc giảm quá giới hạn các số trang - cách dưới đây là cho trang sẽ quay vòng tròn, bạn có thể thay đổi giá trị nếu không muốn quay vòng, hoặc mở rộng hơn làm ẩn luôn nút tăng/giảm khi đến giới hạn
					if now_videopage > len_videos:		#nếu tăng quá tổng số trang
						now_videopage = 1				#đưa số trang quay về đầu
					if now_videopage < 1:				#nếu giảm quá tổng số trang
						now_videopage = len_videos		#đưa số trang về cuối
					if now_playlist > len_playlists:	#nếu tăng quá tổng số playlist
						now_playlist = 1				#đưa về playlist đầu tiên
					if now_playlist < 1:				#nếu giảm quá tổng số playlist
						now_playlist = len_playlists	#đưa về playlist cuối
	
					for i in range(len(videos_btn_list)):	#vòng lặp i chạy đến hết danh sách nút bấm video
						if ((now_videopage-1)*row_video) <= i < (row_video*now_videopage):	#chỉ kiểm tra những vị trí video đủ điều kiện đang được hiện trên trang
							if videos_btn_list[i].is_mouse_on_text():		#nếu bấm vào vị trí 1 video xác định
								playlist.videos[i].open()					#mở video đã ấn vào bằng trình duyệt web thông qua hàm open() đã định nghĩa
								print("đã chọn", playlist.videos[i].title)	#in ra cmd kiểm tra

			if event.type == pygame.QUIT:				#Ấn thoát/tắt chương trình
				running = False							#đưa vòng lặp while về False để thoát
		
		pygame.display.flip()		#làm mới toàn bộ màn hình
		#pygame.display.update() 	#làm mới 1 phần màn hình theo (x,y,độ dài trục x, độ dài trục y)
	pygame.quit()					#thoát pygame

if __name__ == '__main__': main()	#đảm bảo bạn đang chạy trực tiếp chương trình này
else:
	"Chương trình đang được gọi!"	#trường hợp bạn đang gọi chương trình này từ 1 chương trình khác bên ngoài


"""
Lưu ý: Khi đối tượng không được draw() hoặc draw_info() ra thì hàm is_mouse_on_text() sẽ bị lỗi vì không tìm thấy biến text_box
Ngay cả khi trong lệnh if chỉ dùng is_mouse_on_text để check T/F nếu [i] không phải đối tượng đã được vẽ ra cũng sẽ báo lỗi biến text_box
Không can thiệp vào fix cứng vòng lặp for do độ dài danh sách playlist và video không cố định, nếu vòng for lớn hơn len() của danh sách sẽ có lỗi

uỊxq ĐƯỢx uÒkr kÀb yẠk xŨkr gẤe xÓ edb udb hdzk fÁe - lỘe xqƯƠkr egÌkq xqdbỂk ĐỔp xqdỖp fegpkr uỰz VÀj upxepjkzgb. lÌkq mÀl mẬi egÌkq ĐƯỢx lỘe eqỜp rpzk, edb kqpÊk ibeqjk lÌkq xqỈ lỚp yẮe ĐẦd qỌx ĐƯỢx 3 krÀb qÔl kzb, VÌ VẬb egjkr egƯƠkr egÌkq kÀb xÓ eqỂ xÒk kqpỀd qÀl VÀ xÂd mỆkq krẮk rỌk qƠk lÀ lÌkq xqƯz ypẾe ĐỂ uÙkr eỚp, mÀl xjut krẮk rỌk qƠk, qpỆd hdẢ qƠk. VỚp lỤx ĐÍxq xqpz fẺ qỌx eẬi, lÌkq ljkr kqẬk ĐƯỢx kqỮkr iqẢk qỒp ĐỂ qjÀk eqpỆk qƠk. qÃb ldz nqÓz qỌx xqÍkq eqỨx ĐỂ Ủkr qỘ eÁx rpẢ uŨkr mẠp kqÉ! - mjkr
"""
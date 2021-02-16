from requests import get
from scrapy import Selector
import hashlib
import timeit
from threading import Thread

# GLOVAL VARIABLE
OKGREEN = '\033[92m'
WHITE = '\033[0m'

# start timer
start_timer = timeit.default_timer()

# open output file
out = open("digest.out", "w", encoding='utf-8')

# scrapper function, called in each thread
def scrap(i, start, end):
	idx = start
	try:
		print(i,start,end)

		# url tho scrap from
		url = "https://www.challengecybersec.fr/9bcb53d26eab7e9e08cc9ffae4396b48/blog/post/"

		response = get(url+str(idx))
		source = None
		while response.status_code != 404:
			if idx >= end:
				break
			source = response.text
			selector = Selector(text=source)
			digest = selector.xpath('//span/text()').extract()
			try:
				if digest[0]:
					print(digest[0])
			except:
				print("digest not defined")
				break

			encryption[i] += str(digest[0])
			idx += 1
			print(str(idx)+" thread:"+str(i))
			response = get(url+str(idx))

		print(OKGREEN+"[FINISHED] Thread:"+WHITE, i)
	except:
		print("-------------------------------------")
		print("i :",i)
		print("response: ", response)
		print("digest", digest[0])
		print("#### relaunching ####")
		scrap(i, idx, end)

#### threading ####
start = 1
end = 1000/20
encryption = []

for i in range(20):
	encryption.append("") 

threads = []
for i in range(0,20):
	t = Thread(target=scrap, args=[i, start, end])
	start += 50
	end += 50
	threads.append(t)
	t.start()

for thread in threads:
	thread.join()

#### encryption
toEncrypt = ""
for s in encryption:
	toEncrypt += str(s)

print(toEncrypt)

res = hashlib.md5(toEncrypt.encode('utf-8'))

out.write(toEncrypt)
out.write("\n")

out.write("hexadecimal digest : \n")
out.write(str(res.hexdigest()))

out.write("\n")
out.write("digest : \n")
out.write(str(res.digest()))

### stop timer
stop = timeit.default_timer()
print("time: ", stop-start_timer)

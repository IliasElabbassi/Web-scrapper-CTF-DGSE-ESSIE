from requests import get
from scrapy import Selector
import hashlib
import timeit
from threading import Thread

start = timeit.default_timer()

out = open("digest.out", "w", encoding='utf-8')

def scrap(i, start, end):
	try:
		print(i,start,end)
		idx = start

		url = "https://www.challengecybersec.fr/9bcb53d26eab7e9e08cc9ffae4396b48/blog/post/"

		response = get(url+str(idx))

		source = None

		while response.status_code != 404 or idx >= end:
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
			
	except:
		print("-------------------------------------")
		print("i :",i)
		print("response: ", response)
		print("digest", digest[0])
		print("#### relaunching ####")
		scrap(i, idx, end)

#### threading ####
start = 1
end = 1000/10

encryption = []

for i in range(10):
	encryption.append("") 

threads = []

for i in range(0,10):
	t = Thread(target=scrap, args=[i, start, end])
	
	if i == 0:
		start += 99
	else:
		start += 100

	end += 100
	threads.append(t)
	t.start()


for thread in threads:
	thread.join()




#### encryption

toEncrypt = ""
for s in encryption:
	toEncrypt += str(s)

out.write(toEncrypt)
out.write("\n")

print(toEncrypt)
res = hashlib.md5(toEncrypt.encode('utf-8'))

out.write("hexadecimal digest : \n")
out.write(str(res.hexdigest()))

out.write("\n")
out.write("digest : \n")
out.write(str(res.digest()))


stop = timeit.default_timer()

print("time: ", stop-start)
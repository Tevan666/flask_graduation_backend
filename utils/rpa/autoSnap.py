import rpa as r

r.init()
r.url('https://www.bing.com')
r.type('//*[@name="q"]', 'lishenghua[enter]')
print(r.read('result-stats'))
r.snap('page', 'results.png')
r.close()
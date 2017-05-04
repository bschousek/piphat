read_path.py is a proof of concept for using pigpio dma waveforms to generate step pulses from a Raspberry Pi.

Youtube video of successes at [link1](https://www.youtube.com/watch?v=zQGvGT186qI) and [link2](https://www.youtube.com/watch?v=MncD2ePda3s)

I tried to grok the stepgen.c for software pulse generation and think I got it, but found an interesting [article](http://www.eetimes.com/document.asp?doc_id=1276928&page_number=1) so thought I would mess a bit with numpy matrix multiplication which should be pretty snappy.

Let's assume that we want to create 100 kHz step rates. For a servo loop of 1 ms or 1e6 ns that means we could potentially want to create 100 pulses per servo period, or a step every 10e3 ns. Let's try the algorithm from the article at 10 times that rate, checking to see numpy performance at calculating the numbers from Table 1. So we will check speed-time products for 1000 element long arrays. We'll assume full constant speed of 


import threading
import queue
import time
import random

# setup awal
totalJob = 13 
antrian = queue.Queue()

for i in range(1, totalJob + 1):
    antrian.put(i)

# waktu tiap task
data_waktu = []
kunci = threading.Lock()

# fungsi worker
def kerja(nama):
    while not antrian.empty():
        try:
            job = antrian.get_nowait()
        except:
            break

        mulai = time.time()
        print(f"{nama} sedang mengerjakan task ke-{job}")

        lama = random.uniform(0.4, 1.3)
        time.sleep(lama)

        selesai = time.time()
        durasi = selesai - mulai

        print(f"{nama} sudah selesai task {job} (sekitar {round(durasi,2)} detik)")

        # menyimpan waktu
        with kunci:
            data_waktu.append(durasi)

        antrian.task_done()

# bikin processor
list_worker = []
jumlah_worker = 4   

start = time.time()

for i in range(jumlah_worker):
    t = threading.Thread(target=kerja, args=(f"CPU-{i+1}",))
    list_worker.append(t)
    t.start()

for w in list_worker:
    w.join()

end = time.time()

# hasil akhir
total = end - start
rata2 = sum(data_waktu) / len(data_waktu)

print("\n---- RINGKASAN ----")
print(f"Total waktu: {round(total,2)} detik")
print(f"Rata-rata per task: {round(rata2,2)} detik")

print("\nCatatan:")
print("- Task diambil satu-satu dari antrian")
print("- Yang selesai duluan bisa langsung lanjut ambil task lagi")
print("- Jadi walaupun pembagian ga rata, waktu total lebih cepat")
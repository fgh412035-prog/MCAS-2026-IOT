
import RPi.GPIO as GPIO
import time

# 設定使用 BCM 編號系統
GPIO.setmode(GPIO.BCM)

# 超聲波模組的 TRIG 與 ECHO 引腳
TRIG_y = 4
ECHO_r = 18

# 設定引腳輸出入模式
GPIO.setup(TRIG_y, GPIO.OUT)
GPIO.setup(ECHO_r, GPIO.IN)


def measure_distance():
    # 關閉發射端，等待感測器穩定
    GPIO.output(TRIG_y, False)
    time.sleep(0.5)

    # 發送 10 微秒觸發脈衝
    GPIO.output(TRIG_y, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_y, False)

    # 等待 Echo 變成高電位，設定逾時避免程式卡住
    timeout = time.time() + 0.03

    while GPIO.input(ECHO_r) == 0:
        pulse_start = time.time()
        if pulse_start > timeout:
            return None

    # 等待 Echo 變回低電位
    timeout = time.time() + 0.03

    while GPIO.input(ECHO_r) == 1:
        pulse_end = time.time()
        if pulse_end > timeout:
            return None

    # 計算距離
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance


try:
    print("程式啟動，按 Ctrl+C 可以停止測試...")

    while True:

        # LAB4-2：讀取目前距離
        distance = measure_distance()

        if distance is None:
            print("無法取得距離，請檢查感測器接線")
        else:
            # 判斷距離是否小於 20 cm
            if distance < 20:
                status = "注意！！！"
            else:
                status = "沒事"

            # 顯示距離與目前狀態
            print(f"當前距離：{distance} cm，當前狀態：{status}")

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n停止測量中...")

finally:
    GPIO.cleanup()
    print("GPIO 已清理，程式結束。")


import serial
import RPi.GPIO as GPIO

# 設定 GPIO
GPIO.setmode(GPIO.BCM)

LED = 17
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, GPIO.LOW)

# 設定 UART：9600 baud
ser = serial.Serial(
    port='/dev/serial0',
    baudrate=9600,
    timeout=2
)

try:
    print("Lab 4-3 UART 實驗啟動")
    print("請輸入數字或字元，輸入 q 結束")
    print("輸入 1：LED 亮；輸入 0：LED 滅")

    while True:
        # 輸入要傳送的資料
        message = input("請輸入資料：")

        if message.lower() == 'q':
            break

        # 透過 UART 傳送資料
        ser.write((message + '\n').encode('utf-8'))
        ser.flush()

        # 接收 UART 傳回的資料
        received = ser.readline().decode(
            'utf-8', errors='replace'
        ).strip()

        if received:
            print(f"傳送資料：{message}")
            print(f"接收資料：{received}")

            # 依照接收到的資料控制 LED
            if received == '1':
                GPIO.output(LED, GPIO.HIGH)
                print("LED 狀態：亮")
            elif received == '0':
                GPIO.output(LED, GPIO.LOW)
                print("LED 狀態：滅")
            else:
                GPIO.output(LED, GPIO.LOW)
                print("LED 狀態：滅（非 1 或 0）")
        else:
            print("沒有收到資料，請檢查 UART 接線")

except KeyboardInterrupt:
    print("\n停止實驗")

finally:
    GPIO.output(LED, GPIO.LOW)
    ser.close()
    GPIO.cleanup()
    print("UART 與 GPIO 已清理")

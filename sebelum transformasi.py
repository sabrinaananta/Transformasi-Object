import pygame  # pygame digunakan untuk menggambar elemen-elemen tampilan dalam lingkungan grafis.
import sys  # sys digunakan untuk mengelola berbagai aspek sistem seperti keluar dari program.
import math  # digunakan untuk melakukan operasi matematika seperti menghitung trigonometri untuk rotasi objek.
import datetime  # datetime digunakan untuk mendapatkan waktu saat ini guna mengatur rotasi jarum jam.


def draw_table_3d(
    surface,
    table_color,  # Warna meja (RGB tuple) yang akan digunakan.
    leg_color,  # Warna kaki meja (RGB tuple) yang akan digunakan.
    x,  # Koordinat pusat meja dalam sistem koordinat tiga dimensi
    y,
    z,
    width,  # Dimensi meja dalam tiga dimensi (panjang, lebar, kedalaman). Kedalaman tidak digunakan pada program ini.
    height,
    depth,
    leg_width,  # Dimensi kaki meja dalam tiga dimensi (lebar dan tinggi).
    leg_height,
):
    # Gambar bagian atas meja
    pygame.draw.rect(surface, table_color, (x, y, width, height))

    # Gambar kaki meja 1
    pygame.draw.rect(
        surface,
        leg_color,
        (x + width / 4 - leg_width / 2, y + height, leg_width, leg_height),
    )

    # Gambar kaki meja 2
    pygame.draw.rect(
        surface,
        leg_color,
        (x + 3 * width / 4 - leg_width / 2, y + height, leg_width, leg_height),
    )


def draw_whiteboard_scaled(surface, board_color, x, y, z, width, height, scale):
    # Gambar papan tulis dengan skala tertentu
    scaled_width = int(width * scale)
    scaled_height = int(height * scale)
    pygame.draw.rect(surface, board_color, (x, y, scaled_width, scaled_height))


def draw_chair_3d(
    surface, chair_color, x, y, z, width, height, depth, leg_width, leg_height
):
    # Gambar bagian dudukan kursi
    pygame.draw.rect(surface, chair_color, (x, y, width, height))

    # Gambar kaki kursi 1
    pygame.draw.rect(
        surface,
        chair_color,
        (x + width / 4 - leg_width / 2, y + height, leg_width, leg_height),
    )

    # Gambar kaki kursi 2
    pygame.draw.rect(
        surface,
        chair_color,
        (x + 3 * width / 4 - leg_width / 2, y + height, leg_width, leg_height),
    )


def draw_door_3d(surface, door_color, knob_color, x, y, z, width, height, knob_size):
    # Gambar pintu dengan warna tertentu
    pygame.draw.rect(surface, door_color, (x, y, width, height))

    # Gambar gagang pintu
    knob_x = x + width - knob_size
    knob_y = y + height / 2 - knob_size / 2
    pygame.draw.circle(surface, knob_color, (knob_x, knob_y), knob_size // 2)


def draw_clock_3d(
    surface, clock_hand_color, clock_color, x, y, z, radius, rotation_angle
):
    # Gambar lingkaran jam
    pygame.draw.circle(surface, clock_color, (x, y), radius)

    # Hitung sudut rotasi jarum jam dan menit
    hour_angle = rotation_angle
    minute_angle = 2 * rotation_angle  # Sesuaikan kecepatan rotasi jarum jam dan menit

    # Gambar jarum jam
    hour_hand_length = radius // 2
    hour_hand_angle = math.radians(-hour_angle + 90)
    hour_hand_end_x = x + hour_hand_length * math.cos(hour_hand_angle)
    hour_hand_end_y = y + hour_hand_length * math.sin(hour_hand_angle)
    pygame.draw.line(
        surface, clock_hand_color, (x, y), (hour_hand_end_x, hour_hand_end_y), 5
    )

    # Gambar jarum menit
    minute_hand_length = radius - 10
    minute_hand_angle = math.radians(-minute_angle + 90)
    minute_hand_end_x = x + minute_hand_length * math.cos(minute_hand_angle)
    minute_hand_end_y = y + minute_hand_length * math.sin(minute_hand_angle)
    pygame.draw.line(
        surface, clock_hand_color, (x, y), (minute_hand_end_x, minute_hand_end_y), 2
    )


def draw_writing_tools(surface, tool_color, x, y, z, width, height, num_tools):
    # Gambar alat tulis di bawah papan tulis di pinggir kanan
    for i in range(num_tools):
        tool_width_small, tool_height_small = (
            width // 2,
            height // 4,
        )  # Ukuran alat tulis yang lebih kecil
        tool_x = x + i * (width + 10)  # Sesuaikan jarak antar alat tulis
        tool_y, tool_z = (
            y + height * 1.2,
            z + 5,
        )  # Posisi alat tulis di bawah papan tulis, menyesuaikan nilai y dan z
        pygame.draw.rect(
            surface, tool_color, (tool_x, tool_y, tool_width_small, tool_height_small)
        )


def draw_locker_3d(surface, locker_color, x, y, z, width, height, depth):
    # Gambar loker dengan warna tertentu
    pygame.draw.rect(surface, locker_color, (x, y, width, height))


def rotate_point(x, y, center_x, center_y, angle):
    # Rotasi titik (x, y) sekitar pusat (center_x, center_y) sebesar angle derajat
    angle_rad = math.radians(angle)
    x_rotated = (
        center_x
        + (x - center_x) * math.cos(angle_rad)
        - (y - center_y) * math.sin(angle_rad)
    )
    y_rotated = (
        center_y
        + (x - center_x) * math.sin(angle_rad)
        + (y - center_y) * math.cos(angle_rad)
    )
    return x_rotated, y_rotated


def rotate_point_3d(x, y, z, angle):
    # Rotasi titik (x, y, z) sekitar sumbu z sebesar angle derajat
    angle_rad = math.radians(angle)
    x_rotated = x * math.cos(angle_rad) - y * math.sin(angle_rad)
    y_rotated = x * math.sin(angle_rad) + y * math.cos(angle_rad)
    return x_rotated, y_rotated, z


def draw_classroom_3d(
    tool_direction=1, tool_direction_y=1
):  # tambahkan ini jika keatas keabwah tool_direction_y=1  #tool_direction=1 untuk nyalakan translasi rotasi dan scalling
    # Inisialisasi Pygame
    pygame.init()

    # Atur lebar dan tinggi layar
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Classroom Drawing")

    # Warna latar belakang
    background_color = (135, 206, 235)  # Ubah ke skyblue

    # Warna elemen-elemen kelas
    floor_color = (169, 169, 169)  # Abu-abu tua (RGB) untuk lantai
    table_color = (139, 69, 19)  # Coklat (RGB)
    leg_color = (139, 69, 19)  # Coklat (RGB)
    board_color = (0, 0, 0)  # Hitam (RGB) untuk papan tulis
    chair_color = (0, 128, 128)  # Cyan (RGB) untuk kursi
    clock_hand_color = (0, 0, 0)  # Hitam (RGB) untuk jarum jam
    clock_color = (0, 0, 255)  # Biru (RGB) untuk jam
    door_color = (139, 69, 19)  # Coklat (RGB) untuk pintu
    knob_color = (255, 255, 255)  # Putih (RGB) untuk gagang pintu

    # Koordinat pusat meja dalam sistem koordinat 3D
    table_center = (width / 2, height / 2, 0)

    # Koordinat untuk papan tulis di tengah atas
    board_width, board_height = 300, 150  # Ukuran papan tulis yang lebih kecil
    board_x, board_y, board_z = (
        width / 2 - board_width / 2,
        height / 6,
        0,
    )  # Posisi papan tulis di atas tengah (diubah dari height / 4 ke height / 6)

    # Translasi
    # Koordinat untuk alat tulis di atas papan tulis
    tool_width, tool_height = 25, 70  # Ukuran alat tulis
    num_tools = 1  # Ubah sesuai kebutuhan

    tool_x = board_x + board_width - 10
    tool_y = board_y - tool_height - 10
    tool_z = 5

    # Jarak antara meja dan kursi
    distance_between_table_and_chair = 20

    # Koordinat untuk meja di dekat papan tulis di pinggir kanan
    table_width, table_height = 150, 75
    table_x, table_y, table_z = (
        board_x + board_width + distance_between_table_and_chair,
        height / 2 - table_height,
        0,
    )  # Posisi meja di pinggir kanan dekat papan tulis

    # Koordinat untuk loker di pinggir kanan bawah dekat meja
    locker_width, locker_height, locker_depth = 100, 150, 60
    locker_x, locker_y, locker_z = (
        table_x + table_width + 15,
        height / 1.5 + table_height - locker_height + 40,
        0,
    )

    # Koordinat untuk kursi di tengah menghadap papan tulis
    num_chairs_front = 4  # Ubah sesuai kebutuhan
    num_chairs_back = 4  # Ubah sesuai kebutuhan

    chair_width, chair_height = 50, 50
    distance_between_chairs = 30

    total_chairs_width_front = num_chairs_front * chair_width
    total_chairs_width_back = num_chairs_back * chair_width
    total_distance_width_front = (num_chairs_front - 1) * distance_between_chairs
    total_distance_width_back = (num_chairs_back - 1) * distance_between_chairs

    starting_x_front = (
        width - total_chairs_width_front - total_distance_width_front
    ) / 2
    starting_x_back = (width - total_chairs_width_back - total_distance_width_back) / 2

    chair_positions = []

    # Jarak antar kursi di bagian depan
    distance_between_chairs_front = 50

    # Jarak antar kursi di bagian belakang
    distance_between_chairs_back = 70  # Anda dapat mengubah nilai ini sesuai kebutuhan

    # Koordinat untuk kursi di depan papan tulis
    for i in range(num_chairs_front):
        chair_x = starting_x_front + i * (chair_width + distance_between_chairs_front)
        chair_y, chair_z = (
            height / 2 + 50,
            50 + i * 20,
        )  # Menyesuaikan nilai y dan z dengan jarak vertikal
        chair_positions.append((chair_x, chair_y, chair_z))

    # Koordinat untuk kursi di belakang papan tulis
    for i in range(num_chairs_back):
        chair_x = starting_x_back + i * (chair_width + distance_between_chairs_back)
        chair_y, chair_z = (
            height / 2 + chair_height + 10 + 50,
            50 + i * 20,
        )  # Menyesuaikan nilai y dan z dengan jarak vertikal
        chair_positions.append((chair_x, chair_y, chair_z))

    # Koordinat untuk jam di atas papan tulis
    clock_x, clock_y, clock_z = width / 2, board_y - 30, 50
    clock_radius = 20

    clock_angle = 0  # Inisialisasi sudut rotasi jarum jam

    # Koordinat dan ukuran untuk pintu
    door_x, door_y, door_z = 50, height / 2 - 50, 0  # Posisi pintu di sebelah kiri
    door_width, door_height = 40, 150  # Panjang dan lebar pintu yang disesuaikan

    # Ukuran gagang pintu
    knob_size = 10

    # Ukuran meja
    table_width, table_height = 150, 75

    # Ukuran kursi
    chair_width, chair_height = 50, 50

    # Jarak antar kursi
    distance_between_chairs = 30

    # Inisialisasi variabel arah gerakan alat tulis
    tool_direction_local = tool_direction  # Tambahkan variabel lokal di dalam fungsi
    tool_direction_y_local = tool_direction_y

    # Inisialisasi variabel untuk rotasi, translasi, dan scaling
    rotation_angle = 0
    translation_speed = 1

    # Inisialisasi skala papan tulis
    board_scale = 1.0

    # Mulai loop utama
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # # Rotasi kekanan
        # rotation_angle += 0.1  # Sesuaikan dengan kecepatan rotasi yang diinginkan

        # #rotasi ke kiri
        # rotation_angle -= 0.1

        # # Translasi
        # tool_x += translation_speed * tool_direction_local
        # tool_y += translation_speed * tool_direction_y_local

        # # Jika alat tulis mencapai batas kanan atau kiri layar, ubah arah gerakan
        # if tool_x + tool_width > width or tool_x < 0:
        #     tool_direction_local *= -1
        # # Setel posisi alat tulis ke batas yang valid
        #     tool_x = max(0, min(width - tool_width, tool_x))

        # # Jika alat tulis mencapai batas atas atau bawah layar, ubah arah gerakan
        # if tool_y + tool_height > height or tool_y < 0:
        #     tool_direction_y_local *= -1
        # # Setel posisi alat tulis ke batas yang valid
        #     tool_y = max(0, min(height - tool_height, tool_y))

        # #scalling
        # board_scale += 0.0001

        # Gambar latar belakang
        screen.fill(background_color)

        # Gambar lantai
        pygame.draw.rect(screen, floor_color, (0, height / 2, width, height / 2))

        # # Update sudut rotasi jarum jam
        # clock_angle += 0.1  # Sesuaikan dengan kecepatan rotasi yang diinginkan

        # Hitung posisi akhir jarum jam yang sudah dirotasi
        clock_hand_end_x, clock_hand_end_y = rotate_point(
            clock_x, clock_y, clock_x, clock_y, clock_angle
        )

        # Gambar jarum jam dengan posisi akhir yang sudah dirotasi
        pygame.draw.line(
            screen,
            clock_hand_color,
            (clock_x, clock_y),
            (clock_hand_end_x, clock_hand_end_y),
            5,
        )

        # Gambar meja dengan kaki (3 dimensi)
        draw_table_3d(
            screen,
            table_color,
            leg_color,
            table_x,
            table_y,
            table_z,
            table_width,
            table_height,
            50,
            20,
            50,
        )

        draw_whiteboard_scaled(
            screen,
            board_color,
            board_x,
            board_y,
            board_z,
            board_width,
            board_height,
            board_scale,
        )

        # Gambar loker di pinggir kanan bawah dekat meja
        draw_locker_3d(
            screen,
            (255, 0, 0),
            locker_x,
            locker_y,
            locker_z,
            locker_width,
            locker_height,
            locker_depth,
        )

        # Gambar alat tulis di bawah papan tulis
        draw_writing_tools(
            screen,
            (255, 255, 255),
            tool_x,
            tool_y,
            tool_z,
            tool_width,
            tool_height,
            num_tools,
        )

        # Gambar kursi di tengah menghadap papan tulis dengan jarak antar kursi
        for i, (chair_x, chair_y, chair_z) in enumerate(chair_positions):
            draw_chair_3d(
                screen,
                chair_color,
                chair_x,
                chair_y,
                chair_z,
                chair_width,
                chair_height,
                50,
                20,
                50,
            )

        # Gambar jam di atas papan tulis
        draw_clock_3d(
            screen,
            clock_hand_color,
            clock_color,
            clock_x,
            clock_y,
            clock_z,
            clock_radius,
            rotation_angle,
        )

        # Gambar pintu
        draw_door_3d(
            screen,
            door_color,
            knob_color,
            door_x,
            door_y,
            door_z,
            door_width,
            door_height,
            knob_size,
        )

        # Update layar
        pygame.display.flip()

        # Kontrol kecepatan perputaran dengan menambahkan delay
        pygame.time.delay(10)  # Sesuaikan dengan kecepatan rotasi yang diinginkan

    # Hentikan Pygame
    pygame.quit()
    sys.exit()


# Panggil fungsi untuk menggambar kelas
draw_classroom_3d()

import requests

def tra_cuu_tai_khoan():
    """Tra cứu thông tin tài khoản VioTP."""
    token = input("Nhập token API VioTP: ")
   

    while True:
        print("\nChọn thao tác:")
        print("1. Lấy danh sách nhà mạng")
        print("2. Lấy danh sách dịch vụ")
        print("3. Tra cứu thông tin tài khoản")
        print("4. Yêu cầu dịch vụ")
        print("5. lay code")
        print("0. Thoát")

        lua_chon = input("Nhập lựa chọn của bạn: ")

        if lua_chon == "1":
            lay_danh_sach_nha_mang(token)
        elif lua_chon == "2":
            country = input("Nhập mã quốc gia (vn/la): ")
            lay_danh_sach_dich_vu(token, country)
        elif lua_chon == "3":
            tra_cuu_tai_khoan_voi_token(token)
        elif lua_chon == "4":
             service_id = int(input("Nhập ID dịch vụ: "))
             yeu_cau_dich_vu(token, service_id, country="vn", network=None, prefix=None, except_prefix=None, number=None)
        elif lua_chon == "5":
             request_id = int(input("Nhập ID dịch vụ: "))
             get_verification_code(token, request_id)
        elif lua_chon == "0":
            print("Thoát chương trình.")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng nhập lại.")

def tra_cuu_tai_khoan_voi_token(token):
    """Tra cứu thông tin tài khoản VioTP bằng token đã cung cấp."""
    url = f"https://api.viotp.com/users/balance?token={token}"
    response = requests.get(url)

    if response.status_code == 200:
        try:
            data = response.json()

            if "data" in data:
                balance = data["data"]["balance"]
                print(f"Số dư tài khoản: {balance}")
            else:
                print("Không tìm thấy key 'data' trong dữ liệu trả về.")
        except KeyError:
            print("Lỗi: Không thể phân tích dữ liệu trả về.")
    else:
        print(f"Lỗi: {response.status_code}")

def lay_danh_sach_nha_mang(token):
    """Lấy danh sách nhà mạng."""
    url = f"https://api.viotp.com/networks/get?token={token}"
    response = requests.get(url)

    if response.status_code == 200:
        try:
            data = response.json()

            print("\nDanh sách nhà mạng:")
            for nha_mang in data["data"]:
                print(f"{nha_mang['id']}. {nha_mang['name']}")
        except KeyError:
            print("Lỗi: Không thể phân tích dữ liệu trả về.")
    else:
        print(f"Lỗi: {response.status_code}")

def lay_danh_sach_dich_vu(token, country="vn"):
  """Lấy danh sách dịch vụ."""
  url = f"https://api.viotp.com/service/getv2?token={token}&country={country}"
  response = requests.get(url)

  if response.status_code == 200:
    try:
      data = response.json()

      print(f"\nDanh sách dịch vụ ({country.upper()}):")
      # Increased indentation for the loop body
      for dich_vu in data["data"]:
        print(f"{dich_vu['id']}. {dich_vu['name']} - Giá: {dich_vu['price']}")
    except KeyError:
      print("Lỗi: Không thể phân tích dữ liệu trả về.")
  else:
    print(f"Lỗi: {response.status_code}")


import requests

def yeu_cau_dich_vu(token, service_id, country="vn", network=None, prefix=None, except_prefix=None, number=None):
    """Yêu cầu dịch vụ thuê sim VioTP."""
    url = f"https://api.viotp.com/request/getv2?token={token}&serviceId={service_id}"

    if country:
        url += f"&country={country}"

    if network:
        url += f"&network={network}"

    if prefix:
        url += f"&prefix={prefix}"

    if except_prefix:
        url += f"&exceptPrefix={except_prefix}"

    if number:
        url += f"&number={number}"

    response = requests.get(url)

    if response.status_code == 200:
        try:
            data = response.json()

            if "status_code" in data and data["status_code"] == 200:
                if "data" in data:
                    sim_data = data["data"]

                    # Extract and print relevant information from sim_data
                    print(f"\nYêu cầu thành công!")
                    print(f"Số điện thoại đã thuê: {sim_data['phone_number']}")
                    print(f"Giá trị thuê lại: {sim_data['re_phone_number']}")
                    print(f"Mã quốc gia: {sim_data['countryISO']}")
                    print(f"Mã vùng quốc gia: {sim_data['countryCode']}")
                    print(f"Số dư tài khoản: {sim_data['balance']}")
                    print(f"Mã yêu cầu: {sim_data['request_id']}")
                else:
                    print("Không tìm thấy dữ liệu sim trong phản hồi.")
            else:
                print(f"Lỗi: {data['message']}")
        except KeyError:
            print("Lỗi: Không thể phân tích dữ liệu trả về.")
    else:
        print(f"Lỗi: {response.status_code}")

def get_verification_code(token, request_id):
  """Retrieves the verification code for a rented SIM phone number."""
  url = f"https://api.viotp.com/session/getv2?requestId={request_id}&token={token}"
  response = requests.get(url)

  if response.status_code == 200:
    try:
      data = response.json()

      if "status_code" in data and data["status_code"] == 200:
        if "data" in data:
          verification_data = data["data"]

          # Extract and print relevant verification information
          print(f"\nMã xác thực:")
          print(f"Số điện thoại: {verification_data['Phone']}")
          print(f"Mã OTP: {verification_data['Code']}")

          if verification_data["IsSound"]:
            print(f"Link file âm thanh OTP: {verification_data['SmsContent']}")
        else:
          # Indent this line by 4 spaces
          print("Không tìm thấy dữ liệu xác thực trong phản hồi.")
      else:
        print(f"Lỗi: {data['message']}")
    except KeyError:
      print("Lỗi: Không thể phân tích dữ liệu trả về.")
  else:
    print(f"Lỗi: {response.status_code}")


        
# Khởi chạy bot
tra_cuu_tai_khoan()

"""
신분당선 역별 대장주 아파트 가격 변화 조회 서비스
Flask 기반 웹 애플리케이션
"""

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import json
from datetime import datetime, timedelta
import random

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# 역별 아파트 데이터 로드
def load_stations_data():
    with open('stations.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# 아파트 가격 데이터 생성 (실제 API 연동 전 Mock 데이터)
# 실제 서비스에서는 국토교통부 실거래가 API 와 연동
def generate_apartment_price_data(apartment_name, address):
    """
    아파트 가격 변화를 시뮬레이션하는 함수
    실제 구현시에는 국토교통부 실거래가 OpenAPI 를 연동
    """
    # 기본 가격 설정 (단지별 차등화)
    base_prices = {
        '광교': 85000,  # 만원/평
        '수지': 75000,
        '성복': 70000,
        '분당': 95000,
        '판교': 110000,
        '신사': 150000,
        '상현': 80000,
        '미금': 85000,
        '정자': 90000,
        '수내': 88000,
        '삼평': 105000,
        '보라': 100000,
        '하광교': 82000,
    }
    
    base_price = 80000  # 기본값
    for key, price in base_prices.items():
        if key in apartment_name:
            base_price = price
            break
    
    # 가격 변화율 (상승 추세 시뮬레이션)
    changes = {
        '1_month': round(random.uniform(-2, 5), 2),
        '3_months': round(random.uniform(-3, 8), 2),
        '6_months': round(random.uniform(-5, 15), 2),
        '12_months': round(random.uniform(-8, 25), 2),
        '2_years': round(random.uniform(-10, 40), 2),
    }
    
    # 현재 가격
    current_price = base_price + random.randint(-5000, 5000)
    
    # 과거 가격 계산
    price_history = {
        'current': current_price,
        '1_month_ago': round(current_price * (100 - changes['1_month']) / 100, 2),
        '3_months_ago': round(current_price * (100 - changes['3_months']) / 100, 2),
        '6_months_ago': round(current_price * (100 - changes['6_months']) / 100, 2),
        '12_months_ago': round(current_price * (100 - changes['12_months']) / 100, 2),
        '2_years_ago': round(current_price * (100 - changes['2_years']) / 100, 2),
    }
    
    return {
        'apartment_name': apartment_name,
        'address': address,
        'current_price_per_pyung': current_price,  # 만원/평
        'price_changes': changes,
        'price_history': price_history,
        'data_source': '국토교통부 실거래가 API (Mock)',
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')

@app.route('/api/stations')
def get_stations():
    """역 목록 조회"""
    data = load_stations_data()
    return jsonify({
        'success': True,
        'data': data['stations']
    })

@app.route('/api/stations/<int:station_id>')
def get_station(station_id):
    """특정 역 정보 조회"""
    data = load_stations_data()
    for station in data['stations']:
        if station['id'] == station_id:
            return jsonify({
                'success': True,
                'data': station
            })
    return jsonify({
        'success': False,
        'error': 'Station not found'
    }), 404

@app.route('/api/apartment/price')
def get_apartment_price():
    """아파트 가격 정보 조회"""
    apartment_name = request.args.get('name', '')
    address = request.args.get('address', '')
    
    if not apartment_name:
        return jsonify({
            'success': False,
            'error': 'Apartment name is required'
        }), 400
    
    price_data = generate_apartment_price_data(apartment_name, address)
    
    return jsonify({
        'success': True,
        'data': price_data
    })

@app.route('/api/apartments/prices')
def get_apartments_prices():
    """여러 아파트 가격 정보 일괄 조회"""
    apartments = request.args.getlist('apartments')
    addresses = request.args.getlist('addresses')
    
    results = []
    for i, apt_name in enumerate(apartments):
        addr = addresses[i] if i < len(addresses) else ''
        price_data = generate_apartment_price_data(apt_name, addr)
        results.append(price_data)
    
    return jsonify({
        'success': True,
        'data': results
    })

if __name__ == '__main__':
    import os
    print("=" * 60)
    print("신분당선 역별 대장주 아파트 가격 변화 조회 서비스")
    print("=" * 60)
    print("서버가 시작됩니다...")
    
    # 호스팅 서비스 환경 변수에서 포트 읽기
    port = int(os.environ.get('PORT', 5000))
    
    print(f"포트: {port}")
    print("브라우저에서 http://localhost:{port} 으로 접속하세요")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=port)

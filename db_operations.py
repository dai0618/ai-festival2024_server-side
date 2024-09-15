import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='emotion_analysis',
            user='root',
            password='abcd1234'  
        )
        return connection
    except Error as e:
        print(f"データベース接続エラー: {e}")
        return None

def insert_emotion_data(image_name, emotions, dominant_emotion):
    try:
        connection = create_connection()
        if connection is None:
            return

        cursor = connection.cursor()
        query = """
        INSERT INTO emotions 
        (angry, disgust, fear, happy, sad, surprise, neutral, dominant_emotion) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            emotions['angry'],
            emotions['disgust'],
            emotions['fear'],
            emotions['happy'],
            emotions['sad'],
            emotions['surprise'],
            emotions['neutral'],
            dominant_emotion
        )

        cursor.execute(query, values)
        connection.commit()
        print("感情データがデータベースに保存されました")

    except Error as e:
        print(f"データ挿入エラー: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# テスト用の関数
def test_connection():
    conn = create_connection()
    if conn is not None and conn.is_connected():
        print("データベース接続テスト成功")
        conn.close()
    else:
        print("データベース接続テスト失敗")

def get_latest_emotion_data():
    try:
        connection = mysql.connector.connect(
           host='localhost',
            database='emotion_analysis',
            user='root',
            password='abcd1234'
        )
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT angry, disgust, fear, happy, sad, surprise, neutral, dominant_emotion
        FROM emotions
        ORDER BY timestamp DESC
        LIMIT 1
        """
        cursor.execute(query)
        result = cursor.fetchone()
        connection.close()
        return result
    except Error as e:
        print(f"データベースエラー: {e}")
        return None

if __name__ == "__main__":
    test_connection()
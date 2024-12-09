<script>
  import Router from 'svelte-spa-router';
  import routes from './routes';

  const API_KEY = import.meta.env.VITE_OPENAI_API_KEY;
</script>

<div class="sidebar">
  <h2>Menu</h2>
  <nav>
    <a href="#/pdfmanager">PDF 관리</a>
    <a href="#/chatbot">챗봇</a>
    <a href="#/graphview">그래프뷰</a>
  </nav>
</div>

<div class="main-content">
  <div class="hero-section">
    <div class="hero-logo">
      <img src="src/assets/images.png" alt="Smart PDF Logo" />
    </div>
    <div class="hero-text">
      <h1>Find answers<br>through precision</h1>
      <p>We provide a precise and secure<br>document search solution.</p>
    </div>
    <div class="hero-icons">
      <div class="icon">
        <p>Better Security</p>
      </div>
      <div class="icon">
        <p>Better Flexibility</p>
      </div>
      <div class="icon">
        <p>Better Precision</p>
      </div>
    </div>
  </div>
</div>

<style>
  /* Google Fonts - Allerta */
  @import url('https://fonts.googleapis.com/css2?family=Allerta&display=swap');

  body {
    font-family: 'Allerta', sans-serif; /* 글씨체 변경 */
    margin: 0;
    background-color: #f0f2f5;
    color: #333;
    font-size: 18px;
  }

  .sidebar {
    width: 250px;
    background-color: #e07100;
    color: #fff;
    display: flex;
    flex-direction: column;
    padding: 20px;
    position: fixed;
    height: 100vh;
    top: 0;
    left: 0;
    border-radius: 0 15px 15px 0;
    box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  }

  .sidebar h2 {
    font-size: 25px;
    margin-bottom: 20px;
    font-weight: 400;
    padding-bottom: 15px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  }

  .sidebar nav a {
    color: rgba(255, 255, 255, 0.9);
    padding: 12px 15px;
    text-decoration: none;
    font-size: 20px;
    display: block;
    border-radius: 10px;
    margin-bottom: 5px;
    transition: all 0.3s ease;
  }

  .sidebar nav a:hover {
    background-color: rgba(255, 255, 255, 0.1);
    color: #fff;
    transform: translateX(5px);
  }

  .main-content {
    margin-left: 250px;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh; /* 세로 가운데 정렬 */
    background-color: #fff;
  }

  .hero-section {
    text-align: center;
  }

  .hero-logo img {
    width: 300px; /* 로고 크기 */
    height: auto;
    margin-bottom: 40px; /* 로고와 텍스트 간격 */
  }

  .hero-text h1 {
    font-size: 5rem; /* 글씨 크기 */
    font-weight: 400;
    margin: 0;
  }

  .hero-text p {
    font-size: 2rem; /* 글씨 크기 */
    margin: 30px 0;
    color: #555;
  }

  .hero-icons {
    display: flex;
    justify-content: center;
    gap: 50px;
    margin-top: 50px;
  }

  .icon {
    text-align: center;
    max-width: 150px;
  }

  .icon p {
    font-size: 1.5rem; /* 글씨 크기 */
    color: #333;
  }
</style>

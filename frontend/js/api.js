// API 기본 설정
const API_BASE_URL = 'http://54.180.115.140:8000/api'; 

// 로컬 스토리지에서 토큰 가져오기
function getToken() {
    return localStorage.getItem('access_token');
}

// 로컬 스토리지에 토큰 저장
function setToken(token) {
    localStorage.setItem('access_token', token);
}

// 토큰 삭제
function clearToken() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_email');
}

// 로그인 상태 확인
function isLoggedIn() {
    return !!getToken();
}

// API 호출 헬퍼 함수
async function apiCall(endpoint, options = {}) {
    const token = getToken();
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
    };

    if (token && !options.skipAuth) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const config = {
        ...options,
        headers,
    };

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || '요청에 실패했습니다.');
        }

        // 204 No Content는 본문이 없음
        if (response.status === 204) {
            return null;
        }

        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// 인증 API
const authAPI = {
    // 회원가입
    async signup(email, username, password) {
        return await apiCall('/auth/signup', {
            method: 'POST',
            body: JSON.stringify({ email, username, password }),
            skipAuth: true,
        });
    },

    // 로그인
    async login(email, password) {
        const formData = new URLSearchParams();
        formData.append('username', email); // OAuth2는 username 필드 사용
        formData.append('password', password);

        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData,
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || '로그인에 실패했습니다.');
        }

        const data = await response.json();
        setToken(data.access_token);
        localStorage.setItem('user_email', email);
        return data;
    },

    // 로그아웃
    logout() {
        clearToken();
        window.location.href = '/';
    },

    // 내 정보 조회
    async getMe() {
        return await apiCall('/auth/me');
    },
};

// 일기 API
const diaryAPI = {
    // 일기 작성
    async create(title, content) {
        return await apiCall('/diaries', {
            method: 'POST',
            body: JSON.stringify({ title, content }),
        });
    },

    // 내 일기 목록
    async getMyDiaries(skip = 0, limit = 10) {
        return await apiCall(`/diaries?skip=${skip}&limit=${limit}`);
    },

    // 모든 일기 목록
    async getAllDiaries(skip = 0, limit = 10) {
        return await apiCall(`/diaries/all?skip=${skip}&limit=${limit}`, {
            skipAuth: true,
        });
    },

    // 특정 일기 조회
    async get(id) {
        return await apiCall(`/diaries/${id}`, { skipAuth: true });
    },

    // 일기 수정
    async update(id, title, content) {
        const updates = {};
        if (title) updates.title = title;
        if (content) updates.content = content;
        
        return await apiCall(`/diaries/${id}`, {
            method: 'PUT',
            body: JSON.stringify(updates),
        });
    },

    // 일기 삭제
    async delete(id) {
        return await apiCall(`/diaries/${id}`, {
            method: 'DELETE',
        });
    },
};

// 질문 API
const questionAPI = {
    // 질문 목록
    async getAll(skip = 0, limit = 10) {
        return await apiCall(`/questions?skip=${skip}&limit=${limit}`, {
            skipAuth: true,
        });
    },

    // 랜덤 질문
    async getRandom() {
        return await apiCall('/questions/random', { skipAuth: true });
    },

    // 특정 질문
    async get(id) {
        return await apiCall(`/questions/${id}`, { skipAuth: true });
    },

    // 전체 개수
    async getCount() {
        return await apiCall('/questions/count/total', { skipAuth: true });
    },
};

// 명언 API
const quoteAPI = {
    // 명언 목록
    async getAll(skip = 0, limit = 10, author = null) {
        let url = `/quotes?skip=${skip}&limit=${limit}`;
        if (author) {
            url += `&author=${encodeURIComponent(author)}`;
        }
        return await apiCall(url, { skipAuth: true });
    },

    // 랜덤 명언
    async getRandom() {
        return await apiCall('/quotes/random', { skipAuth: true });
    },

    // 특정 명언
    async get(id) {
        return await apiCall(`/quotes/${id}`, { skipAuth: true });
    },

    // 작가 목록
    async getAuthors() {
        return await apiCall('/quotes/authors', { skipAuth: true });
    },

    // 전체 개수
    async getCount() {
        return await apiCall('/quotes/count/total', { skipAuth: true });
    },
};

// UI 헬퍼 함수
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error fade-in';
    errorDiv.textContent = message;
    
    const container = document.querySelector('.container');
    container.insertBefore(errorDiv, container.firstChild);
    
    setTimeout(() => errorDiv.remove(), 5000);
}

function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'success fade-in';
    successDiv.textContent = message;
    
    const container = document.querySelector('.container');
    container.insertBefore(successDiv, container.firstChild);
    
    setTimeout(() => successDiv.remove(), 3000);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('ko-KR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
    });
}

// 페이지 로드 시 로그인 상태 확인
function checkAuth() {
    const userEmail = localStorage.getItem('user_email');
    const userInfo = document.getElementById('user-info');
    const authLinks = document.getElementById('auth-links');
    
    if (userInfo && authLinks) {
        if (isLoggedIn() && userEmail) {
            userInfo.style.display = 'flex';
            authLinks.style.display = 'none';
            document.getElementById('user-email').textContent = userEmail;
        } else {
            userInfo.style.display = 'none';
            authLinks.style.display = 'flex';
        }
    }
}

// 페이지 로드 시 실행
document.addEventListener('DOMContentLoaded', checkAuth);


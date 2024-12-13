export interface Task {
    id: number;
    name: string;
    completed: boolean;
    category: Category;
}

export interface Category {
    name: string;
}

export interface User {
    id: number;
    email: string;
    created_at: string;
}

export interface AuthResponse {
    access_token: string;
    token_type: string;
}

export type MessageType = 'error' | 'success' | null;

export type User = {
  first_name: string
  last_name: string
  email: string
}

export async function fetchCheckUserLoggedIn() {
  try {
    const result = await 
    fetch("http://localhost:8000/login", {
      credentials: "include",
      method: "GET",
    }) 
      
    return result.json() as unknown as {user: User, message: string} 
  } catch (error) {
    console.log(error)
    throw error
  }
}


export const fetchLogout = async () => {
  const response = await fetch("http://localhost:8000/logout", {
    method: "POST",
    credentials: "include",
  })

  return response.json()
};


export const fetchLogin = async (email: string, password: string) => {
  const response = await fetch("http://localhost:8000/login", {
    credentials: "include",
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    },
    body: new URLSearchParams({
      username: email,
      password: password,
    }),
  })

  return await response.json() as {user: User}
}



type UserCreate = {
  email: string
  password: string
  first_name: string
  last_name: string
}
export const fetchSignUp = async (data: UserCreate) => {
  const response = await fetch("http://localhost:8000/users", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email: data.email,
      password: data.password,
      first_name: data.first_name,
      last_name: data.last_name,
    }),
  })

  return await response.json()
}
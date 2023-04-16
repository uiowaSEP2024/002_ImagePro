export async function checkUserLoggedIn() {
  try {
    let result = await 
    fetch("http://localhost:8000/login", {
      credentials: "include",
      method: "GET",
    }) 
      
    let data = result.json()
    return data
      
  } catch (error) {
    console.log(error)
    throw error
  }
}

/**
 * Sends the request to initiate a user signup
 * @param email 
 * @param password 
 * @param firstName 
 * @param lastName 
 * @returns 
 */
export const fetchSignUp = async (email: string, password: string, firstName: string, lastName: string) => {
  const response = await fetch("http://localhost:8000/users", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email: email,
      password: password,
      first_name: firstName,
      last_name: lastName,
    }),
  });
  
  return await response.json();
}

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
  });
  
  return await response.json();
}




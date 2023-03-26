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
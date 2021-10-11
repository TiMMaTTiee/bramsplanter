import axios from 'axios'
/* eslint-disable */
export default {
    verifyUser(payload) {
        const path = `http://localhost:5000/api/verify_user`
        return axios({
            method: 'get', 
            url: path,
            auth: {
              username: payload.username,
              password: payload.password
            }
        })
        .then(response => response.data)
        .catch((error) => {
            // eslint-disable-next-line
            console.error(error)
        });
    }
  }

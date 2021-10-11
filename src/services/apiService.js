import axios from 'axios'

var baseUrl = 'http://localhost:5000/api'
/* eslint-disable */
export default {
    async apiRequest(path, args) {
        let full_url = baseUrl.concat(`/${path}`)
        args.forEach(function (arg, index){
            full_url = full_url.concat(`/${arg}`)
        })
        let response
        try {
            response = await axios.get(full_url)
            return response
        }
        catch(error) {
            console.log(error)
        }
    },
    async zipRequest(path) {
        let full_url = baseUrl.concat(path)
        axios({
            url: full_url, 
            method: 'GET',
            responseType: 'blob', 
          }).then((response) => {
             const url = window.URL.createObjectURL(new Blob([response.data]))
             const link = document.createElement('a')
             link.href = url
             link.setAttribute('download', 'logs.zip')
             document.body.appendChild(link)
             link.click()
          })
        
    }
}

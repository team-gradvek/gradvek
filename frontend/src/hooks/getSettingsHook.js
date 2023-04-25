import useSWR from 'swr'
import axios from 'axios'

function getSettings(path) {

  console.log(`This is the path: ${path}`)
  const fetcher = url => axios.get(url).then(res => res.data)

  const { data, error, isLoading } = useSWR(`http://localhost:8000/${path}`, fetcher)
  console.log("Data Returned from Axios")
  console.log(data)
 
  return {
    data: data,
    isLoading,
    isError: error
  }
}

export default getSettings;
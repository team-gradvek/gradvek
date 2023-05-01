import useSWR from 'swr'
import axios from 'axios'

function getSettings(path) {
  
  const fetcher = url => axios.get(url).then(res => res.data)

  const { data, error, isLoading } = useSWR(`http://localhost:8000/${encodeURIComponent(path)}`, fetcher)
 
  return {
    data: data,
    isLoading,
    isError: error
  }
}

export default getSettings;
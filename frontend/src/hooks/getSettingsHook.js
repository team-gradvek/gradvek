import useSWR from 'swr'
import axios from 'axios'

function getSettings(path) {
  
  const fetcher = url => axios.get(url).then(res => res.data)

  const { data, error, isLoading } = useSWR(`http://www.gradvek.org:8083/${encodeURIComponent(path)}`, fetcher)
 
  return {
    data: data,
    isLoading,
    isError: error
  }
}

export default getSettings;

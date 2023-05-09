import useSWR from 'swr'
import axios from 'axios'

function getTargetData(id) {

  const fetcher = url => axios.get(url).then(res => res.data)

  const { data, error, isLoading } = useSWR(`http://localhost:8000/api/ae-weight/${encodeURIComponent(id)}`, fetcher)
  
  return {
    data: data,
    isLoading,
    isError: error
  }
}

export default getTargetData;
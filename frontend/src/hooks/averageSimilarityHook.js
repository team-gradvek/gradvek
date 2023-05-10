import useSWR from 'swr'
import axios from 'axios'

function averageSimilarityHook(id) {

  console.log(`Target passed to Axios: ${id}`)

  const fetcher = url => axios.get(url).then(res => res.data)

  const { data, error, isLoading } = useSWR(`http://localhost:8000/api/average_similarity/${encodeURIComponent(id)}/`, fetcher)

  console.log(data)
  
  return {
    data: data,
    isLoading,
    isError: error
  }
}

export default averageSimilarityHook;
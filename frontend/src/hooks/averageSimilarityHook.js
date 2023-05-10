import useSWR from 'swr'
import axios from 'axios'

function averageSimilarityHook(target) {

  console.log(`Target passed to Axios: ${target}`)

  const fetcher = url => axios.get(url).then(res => res.data)

  const { data, error, isLoading } = useSWR(`http://localhost:8000/api/average_similarity/${encodeURIComponent(target)}`, fetcher)

  console.log(data)
  
  return {
    data: data,
    isLoading,
    isError: error
  }
}

export default averageSimilarityHook;
import useSWR from 'swr'
import axios from 'axios'

function targetSimilarityHook(descriptor, target) {

  const fetcher = url => axios.get(url).then(res => res.data)

  const { data, error, isLoading } = useSWR(`http://www.gradvek.org:8083/api/similarity/${encodeURIComponent(descriptor)}/${encodeURIComponent(target)}`, fetcher)
  
  return {
    data: data,
    isLoading,
    isError: error
  }
}

export default targetSimilarityHook;

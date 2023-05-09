import useSWR from 'swr'
import axios from 'axios'

function getAdverseEvent(id) {

  const fetcher = url => axios.get(url).then(res => res.data)

  const { data, error, isLoading } = useSWR(`http://www.gradvek.org:8083/api/weight/${encodeURIComponent(id)}`, fetcher)
  
  return {
    adverseEvent: data,
    isLoading,
    isError: error
  }
}

export default getAdverseEvent;

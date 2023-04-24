import useSWR from 'swr'
import axios from 'axios'

function getAdverseEvent(id) {

  console.log(`This is the ID: ${id}`)
  const fetcher = url => axios.get(url).then(res => res.data)

  const { data, error, isLoading } = useSWR(`http://localhost:8000/api/weight/${id}`, fetcher)
  console.log(data)
 
  return {
    adverseEvent: data,
    isLoading,
    isError: error
  }
}

export default getAdverseEvent;
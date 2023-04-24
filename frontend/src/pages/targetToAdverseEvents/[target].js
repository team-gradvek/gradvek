import { useRouter } from 'next/router'
import DataTable from '@/components/results/DataTable'
import getAdverseEvent from "../../hooks/targetToAdverseEventHook"
import DataTableSkeleton from '@/components/results/DataTableSkeleton'

const columns = [
  {
    id: 1,
    name: 'Adverse Event'
  }, 
  {
    id: 2,
    name: 'ID'

  },
  {
    id: 3,
    name: 'Weights'
  },
  {
    id: 4,
    name: 'Dataset'
  }
]


const TargetToAdverseEvents = () => {

  // Get data from URL
  const router = useRouter()
  const dataFromURL  = router.query
  const target = dataFromURL.target

  const { adverseEvent, isLoading, isError } = getAdverseEvent(target)

  if (isError) return <p>Failed to Load</p>

  if (isLoading) {
    return (
      <>
        <DataTableSkeleton />
      </>
    )
  }

  return (
    <>
      <DataTable
          title={`Adverse Events for ${target}`}
          data={adverseEvent}
          id={target} 
          columns={columns}
          />
    </>
  )
}

export default TargetToAdverseEvents
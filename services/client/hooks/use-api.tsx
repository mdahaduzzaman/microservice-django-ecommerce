import React from 'react'
import useInterceptor from './use-interceptor'

function useAPI() {
    const publicAxios = useInterceptor()

    
  return (
    <div>useAPI</div>
  )
}

export default useAPI
import React from 'react'

import useFetch from '../../../../hooks/useFetch'
import LoadingComponent from '../components/LoadingComponent.js';
import ErrorComponent from '../components/ErrorComponent.js';

import { fetchTypes } from '../../../../utils/types.ts';

const SolCounter = () => {
  const {data, loading, error} = useFetch(fetchTypes.COORDS)

  if (loading) {
    return (
      <LoadingComponent/>
    )
  } else if (error) {
    return (
      <ErrorComponent />
    )
  } else { 
    return (
      <h3 className='solCounter'>Sol: {data[data.length - 1] ? data[data.length - 1]['sol']:'Not found'}</h3>
    )
  }
}

export default SolCounter
import React from 'react'
import './pagination.scss'

const Pagination = ({ nPages, currentPage, setCurrentPage }) => {

    const pageNumbers = [...Array(nPages + 1).keys()].slice(1)
    const goToNextPage = () => {
            if(currentPage !== nPages) setCurrentPage(currentPage + 1)
    }
    const goToPrevPage = () => {
        if(currentPage !== 1) setCurrentPage(currentPage - 1)
    }
    const goToFirstPage = () => {
        setCurrentPage(1)
    }
    const goToEndPage = () => {
        setCurrentPage(nPages)
    }
    return (
        <nav>
            <ul className='pagination justify-content-center'>
                <li className="page-item">
                    <a className="page-nav border border-0"
                       onClick={goToFirstPage}
                       href='#'>
                        <i className="h5 bi bi-chevron-double-left text-secondary ms-1 square-dim"></i>
                    </a>
                </li>
                <li className="page-item">
                    <a className="page-nav border border-0"
                       onClick={goToPrevPage}
                       href='#'>
                        <i className="h5 bi bi-chevron-left text-secondary ms-1 square-dim"></i>
                    </a>
                </li>
                <li className="page-item">
                    <a className="page-nav border border-0 text-secondary"
                       href='#'>

                        <span className="square-dim">{currentPage}</span>
                    </a>
                </li>
                <li className="page-item">
                    <span className="border border-0 text-secondary size-text-page-nav">
                        of
                    </span>
                </li>
                <li className="page-item">
                    <a className="page-nav border border-0 text-secondary"
                       onClick={() => setCurrentPage(nPages)}
                       href='#'>

                        <span className="square-dim">{nPages}</span>
                    </a>
                </li>
                <li className="page-item">
                    <a className="page-nav border border-0"
                       onClick={goToNextPage}
                       href='#'>
                        <i className="h5 bi bi-chevron-right text-secondary ms-1 square-dim"></i>
                    </a>
                </li>
                <li className="page-item">
                    <a className="page-nav border border-0"
                       onClick={goToEndPage}
                       href='#'>
                        <i className="h5 bi bi-chevron-double-right text-secondary ms-1 square-dim"></i>
                    </a>
                </li>
            </ul>
        </nav>
    )
}

export default Pagination
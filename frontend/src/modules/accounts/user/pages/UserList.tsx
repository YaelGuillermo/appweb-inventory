import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { AppDispatch, RootState } from '@/redux/store'
import { fetchUsers } from '@/redux/actions/accounts/userActions'
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from '@/components/ui/pagination'
import { Spinner, Card, Input } from '@/components/index'
import {
  NotFound,
  Unauthorized,
  Forbidden,
  ServerError,
} from '@/modules/base/index'
import { Edit } from '@geist-ui/icons'
import CreateUserModal from '../../auth/components/CreateUserModal'
import { User } from '@/redux/models/accounts'
import { hasPermission } from '@/utils/permissions'

const UserList: React.FC = () => {
  const dispatch: AppDispatch = useDispatch()
  const navigate = useNavigate()
  const { users, loading, status, error, pagination } = useSelector(
    (state: RootState) => state.user,
  )
  const { user } = useSelector((state: RootState) => state.auth)
  const [searchTerm, setSearchTerm] = useState('')

  const handlePageChange = (page: number) => {
    if (page >= 1 && page <= (pagination?.totalPages || 1)) {
      dispatch(fetchUsers(page, searchTerm))
    }
  }

  useEffect(() => {
    dispatch(fetchUsers(1, searchTerm))
  }, [dispatch, searchTerm])

  const createPageLinks = () => {
    const pages = []
    const totalPages = pagination?.totalPages || 1

    for (let i = 1; i <= totalPages; i++) {
      pages.push(
        <PaginationItem key={i}>
          <PaginationLink
            onClick={() => handlePageChange(i)}
            className={
              pagination?.currentPage === i
                ? 'font-bold cursor-pointer'
                : 'cursor-pointer'
            }
          >
            {i}
          </PaginationLink>
        </PaginationItem>,
      )
    }
    return pages
  }

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value)
  }

  const handleSettings = (id: string) => {
    navigate(`/usuarios/${id}`)
  }

  if (error) {
    if (status === 401) return <Unauthorized />
    if (status === 403) return <Forbidden />
    if (status === 404) return <NotFound />
    if (status === 500) return <ServerError />
  }

  return (
    <Card className="p-6 bg-gray-100">
      <div className="mb-4 flex justify-between">
        <h2 className="text-2xl font-bold mb-4 text-gray-800">Usuarios</h2>
        {hasPermission(user?.role, ['ADMIN']) && <CreateUserModal />}
      </div>
      <Input
        type="text"
        placeholder="Buscar por nombre, correo o rol"
        value={searchTerm}
        onChange={handleSearchChange}
        className="mb-4"
      />
      {loading ? (
        <Spinner />
      ) : users.length === 0 ? (
        <div className="text-gray-500">No hay usuarios.</div>
      ) : (
        <>
          <Table className="min-w-full bg-white rounded-lg shadow-md">
            <TableCaption className="text-gray-500">
              {pagination?.totalItems} usuario(s) encontrado(s).
            </TableCaption>
            <TableHeader>
              <TableRow className="bg-gray-200">
                <TableHead className="px-4 py-2 text-left text-gray-600">
                  Correo electrónico
                </TableHead>
                <TableHead className="px-4 py-2 text-left text-gray-600">
                  Nombre completo
                </TableHead>
                <TableHead className="px-4 py-2 text-left text-gray-600">
                  Género
                </TableHead>
                <TableHead className="px-4 py-2 text-left text-gray-600">
                  Edad
                </TableHead>
                <TableHead className="px-4 py-2 text-left text-gray-600">
                  Rol(es)
                </TableHead>
                <TableHead className="px-4 py-2 text-left"></TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {users.map((user: User) => (
                <TableRow key={user.id} className="hover:bg-gray-100">
                  <TableCell className="px-4 py-2 border-b border-gray-200">
                    {user.email}
                  </TableCell>
                  <TableCell className="px-4 py-2 border-b border-gray-200">
                    {user.first_name} {user.last_name}
                  </TableCell>
                  <TableCell className="px-4 py-2 border-b border-gray-200">
                    {user.profile.gender_display}
                  </TableCell>
                  <TableCell className="px-4 py-2 border-b border-gray-200">
                    {user.profile.age !== null ? user.profile.age : 'No'}
                  </TableCell>
                  <TableCell className="px-4 py-2 border-b border-gray-200">
                    {user.role_display}
                  </TableCell>
                  <TableCell className="px-4 py-2 border-b border-gray-200 text-right">
                    <Edit
                      size={20}
                      className="text-impactBlue cursor-pointer"
                      onClick={() => handleSettings(user.id)}
                    />
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
          <div className="flex justify-between items-center mt-4">
            <Pagination>
              <PaginationContent>
                <PaginationItem>
                  <PaginationPrevious
                    className="cursor-pointer"
                    onClick={() =>
                      handlePageChange(pagination!.currentPage - 1)
                    }
                  />
                </PaginationItem>
                {createPageLinks()}
                <PaginationItem>
                  <PaginationNext
                    className="cursor-pointer"
                    onClick={() =>
                      handlePageChange(pagination!.currentPage + 1)
                    }
                  />
                </PaginationItem>
              </PaginationContent>
            </Pagination>
          </div>
        </>
      )}
    </Card>
  )
}

export default UserList

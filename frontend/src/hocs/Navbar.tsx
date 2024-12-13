import React from 'react'
import { useNavigate } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { AppDispatch, RootState } from '@/redux/store'
import { LogOut, User, Menu } from '@geist-ui/icons'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { logout } from '@/redux/slices/accounts/authSlice'

interface NavbarProps {
  isAuthenticated: boolean
  setSidebarOpen: (open: boolean) => void
  sidebarOpen: boolean
}

const GuestNavbar: React.FC = () => {
  const navigate = useNavigate()
  const handleLogin = () => {
    navigate('/login')
  }
  return (
    <nav className="w-full bg-impactBlue text-white flex flex-col md:flex-row justify-between items-center shadow-lg py-4">
      <div className="flex items-center space-x-4 ml-4">
        <span className="font-bold text-lg">Inventario ITT</span>
      </div>
      <div className="flex items-center space-x-4 mr-4">
        <span
          className="cursor-pointer font-bold text-lg"
          onClick={handleLogin}
        ></span>
      </div>
    </nav>
  )
}

const AuthenticatedNavbar: React.FC<{
  setSidebarOpen: (open: boolean) => void
  sidebarOpen: boolean
}> = ({ setSidebarOpen, sidebarOpen }) => {
  const navigate = useNavigate()
  const dispatch = useDispatch<AppDispatch>()
  const { user } = useSelector((state: RootState) => state.auth)
  const handleLogout = () => {
    dispatch(logout())
    navigate('/login')
  }
  const handleProfile = () => {
    navigate('/me')
  }
  return (
    <nav className="w-full bg-impactBlue text-white flex flex-col md:flex-row justify-between items-center shadow-lg py-4">
      <div className="flex items-center space-x-4 ml-4">
        <span
          className="cursor-pointer p-2"
          onClick={() => setSidebarOpen(!sidebarOpen)}
        >
          <Menu className="h-6 w-6" />
        </span>
        <span className="font-bold text-lg">Inventario ITT</span>
      </div>
      <div className="flex items-center space-x-4 mr-4">
        <span
          className="p-2 rounded flex items-center cursor-pointer"
          onClick={handleProfile}
        >
          {user?.first_name} {user?.last_name}
          <Avatar className="ml-2">
            <AvatarImage src="https://github.com/shadcn.png" />
            <AvatarFallback>a</AvatarFallback>
          </Avatar>
        </span>
        <span
          className="p-2 rounded flex items-center cursor-pointer"
          onClick={handleLogout}
        >
          <span className="mr-2">Cerrar sesión</span>{' '}
          <LogOut className="h-6 w-6" />
        </span>
      </div>
    </nav>
  )
}

const Navbar: React.FC<NavbarProps> = ({
  isAuthenticated,
  setSidebarOpen,
  sidebarOpen,
}) => {
  return isAuthenticated ? (
    <AuthenticatedNavbar
      setSidebarOpen={setSidebarOpen}
      sidebarOpen={sidebarOpen}
    />
  ) : (
    <GuestNavbar />
  )
}

export default Navbar

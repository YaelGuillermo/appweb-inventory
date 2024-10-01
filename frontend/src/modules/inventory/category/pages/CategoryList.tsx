import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { AppDispatch, RootState } from "@/redux/store";
import { fetchCategories } from "@/redux/actions/inventory/categoryActions";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";
import { Spinner, Card, Input } from "@/components/index";
import { Edit } from "@geist-ui/icons";
import CreateCategoryModal from "../components/CreateCategoryModal";
import { Category } from "@/redux/models/inventory";

const CategoryList: React.FC = () => {
  const dispatch: AppDispatch = useDispatch();
  const navigate = useNavigate();
  const { categories, loading, error, pagination } = useSelector(
    (state: RootState) => state.category
  );
  const [searchTerm, setSearchTerm] = useState("");

  const handlePageChange = (page: number) => {
    if (page >= 1 && page <= (pagination?.totalPages || 1)) {
      dispatch(fetchCategories(page, searchTerm));
    }
  };

  useEffect(() => {
    dispatch(fetchCategories(1, searchTerm));
  }, [dispatch, searchTerm]);

  const createPageLinks = () => {
    const pages = [];
    const totalPages = pagination?.totalPages || 1;

    for (let i = 1; i <= totalPages; i++) {
      pages.push(
        <PaginationItem key={i}>
          <PaginationLink
            onClick={() => handlePageChange(i)}
            className={
              pagination?.currentPage === i
                ? "font-bold cursor-pointer"
                : "cursor-pointer"
            }
          >
            {i}
          </PaginationLink>
        </PaginationItem>
      );
    }
    return pages;
  };

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
  };

  const handleSettings = (id: string) => {
    navigate(`/categorys/${id}`);
  };

  return (
    <Card className="p-6 bg-gray-100">
      <div className="mb-4 flex justify-between">
        <h2 className="text-2xl font-bold mb-4 text-gray-800">Partidas</h2>
        <CreateCategoryModal />
      </div>
      <Input
        type="text"
        placeholder="Buscar por nombre o campus"
        value={searchTerm}
        onChange={handleSearchChange}
        className="mb-4"
      />
      {loading ? (
        <Spinner />
      ) : error ? (
        <div className="text-red-500">{error}</div>
      ) : (
        <>
          <Table className="min-w-full bg-white rounded-lg shadow-md">
            <TableCaption className="text-gray-500">
              {pagination?.totalItems} partida(s) fueron encontradas.
            </TableCaption>
            <TableHeader>
              <TableRow className="bg-gray-200">
                <TableHead className="px-4 py-2 text-left text-gray-600">
                  Código
                </TableHead>
                <TableHead className="px-4 py-2 text-left text-gray-600">
                  Nombre
                </TableHead>
                <TableHead className="px-4 py-2 text-left text-gray-600">
                  Descripción
                </TableHead>
                <TableHead className="px-4 py-2 text-left"></TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {categories.map((category: Category) => (
                <TableRow key={category.id} className="hover:bg-gray-100">
                  <TableCell className="px-4 py-2 border-b border-gray-200">
                    {category.code}
                  </TableCell>
                  <TableCell className="px-4 py-2 border-b border-gray-200">
                    {category.name}
                  </TableCell>
                  <TableCell className="px-4 py-2 border-b border-gray-200">
                    {category.description}
                  </TableCell>
                  <TableCell className="px-4 py-2 border-b border-gray-200 text-right">
                    <Edit
                      size={20}
                      className="text-impactBlue cursor-pointer"
                      onClick={() => handleSettings(category.id)}
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
                    disabled={pagination?.currentPage <= 1}
                  />
                </PaginationItem>
                {createPageLinks()}
                <PaginationItem>
                  <PaginationNext
                    className="cursor-pointer"
                    onClick={() =>
                      handlePageChange(pagination!.currentPage + 1)
                    }
                    disabled={pagination?.currentPage >= pagination?.totalPages}
                  />
                </PaginationItem>
              </PaginationContent>
            </Pagination>
          </div>
        </>
      )}
    </Card>
  );
};

export default CategoryList;
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { AppDispatch, RootState } from "@/redux/store";
import { fetchTransactions } from "@/redux/actions/inventory/inventoryTransactionActions";
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
import { Spinner, Card, Input, Badge } from "@/components/index";
import { Edit } from "@geist-ui/icons";
import CreateTransactionModal from "../components/CreateTransactionModal";
import { InventoryTransaction } from "@/redux/models/inventory";

const TransactionList: React.FC = () => {
  const dispatch: AppDispatch = useDispatch();
  const navigate = useNavigate();
  const { transactions, loading, error, pagination } = useSelector(
    (state: RootState) => state.inventoryTransaction
  );
  const [searchTerm, setSearchTerm] = useState("");

  const handlePageChange = (page: number) => {
    if (page >= 1 && page <= (pagination?.totalPages || 1)) {
      dispatch(fetchTransactions(page, searchTerm));
    }
  };

  useEffect(() => {
    dispatch(fetchTransactions(1, searchTerm));
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
    navigate(`/transactions/${id}`);
  };

  const getBadgeColor = (movemenent: string) => {
    switch (movemenent) {
      case "Entrada":
        return "bg-green-400";
      case "Salida":
        return "bg-red-400";
      default:
        return "bg-gray-400";
    }
  };

  return (
    <Card className="p-6 bg-gray-100">
      <div className="mb-4 flex justify-between">
        <h2 className="text-2xl font-bold mb-4 text-gray-800">Transacciones</h2>
        <CreateTransactionModal />
      </div>
      <Input
        type="text"
        placeholder="Buscar por"
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
              {pagination?.totalItems} transaccion(es) encontrada(s).
            </TableCaption>
            <TableHeader>
              <TableRow className="bg-gray-200">
                <TableHead className="px-4 py-2 text-left text-gray-600">
                  Persona
                </TableHead>
                <TableHead className="px-4 py-2 text-left text-gray-600">
                  Producto
                </TableHead>
                <TableHead className="px-4 py-2 text-left text-gray-600">
                  Locación
                </TableHead>
                <TableHead className="px-4 py-2 text-left text-gray-600">
                  Campus
                </TableHead>
                <TableHead className="px-4 py-2 text-left text-gray-600">
                  Cantidad
                </TableHead>
                <TableHead className="px-4 py-2 text-left text-gray-600">
                  Movimiento
                </TableHead>
                <TableHead className="px-4 py-2 text-left text-gray-600">
                  Concepto
                </TableHead>
                <TableHead className="px-4 py-2 text-left text-gray-600">
                  Fecha
                </TableHead>
                <TableHead className="px-4 py-2 text-left"></TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {transactions.map((transaction: InventoryTransaction) => (
                <TableRow key={transaction.id} className="hover:bg-gray-100">
                  <TableCell className="px-4 py-2 border-b border-gray-200">
                    {transaction.person?.first_name}{" "}
                    {transaction.person?.last_name}
                  </TableCell>
                  <TableCell className="px-4 py-2 border-b border-gray-200">
                    {transaction.inventory.product.name}
                  </TableCell>
                  <TableCell className="px-4 py-2 border-b border-gray-200">
                    {transaction.inventory.location.name}
                  </TableCell>
                  <TableCell className="px-4 py-2 border-b border-gray-200">
                    {transaction.inventory.location.warehouse.name}
                  </TableCell>
                  <TableCell className="px-4 py-2 border-b border-gray-200">
                    {transaction.quantity}
                  </TableCell>
                  <TableCell className="px-4 py-2 border-b border-gray-200">
                    <Badge
                      className={getBadgeColor(transaction.movement_display)}
                    >
                      {transaction.movement_display}
                    </Badge>
                  </TableCell>
                  <TableCell className="px-4 py-2 border-b border-gray-200">
                    {transaction.type_display}
                  </TableCell>
                  <TableCell className="px-4 py-2 border-b border-gray-200">
                    {transaction.created_at}
                  </TableCell>
                  <TableCell className="px-4 py-2 border-b border-gray-200 text-right">
                    <Edit
                      size={20}
                      className="text-impactBlue cursor-pointer"
                      onClick={() => handleSettings(transaction.id)}
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

export default TransactionList;
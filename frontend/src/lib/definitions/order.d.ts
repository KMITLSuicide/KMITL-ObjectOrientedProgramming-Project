export interface AllOrderItem {
  id: string;
  price: number;
  status: boolean;
}

export interface Order extends AllOrderItem {
  course_list_name: string[];
  payment_method: string;
  address: string;
  time_stamp: number;
}
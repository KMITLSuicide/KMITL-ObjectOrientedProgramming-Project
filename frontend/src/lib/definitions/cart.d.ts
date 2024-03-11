export interface PaymentMethod {
  name: string;
}

export interface PaymentMethodWithID extends PaymentMethod {
  id: string;
}

export interface BuyPostData {
  address: string;
  is_paid: boolean;
  payment_method: string;
}

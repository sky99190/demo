#include <stdio.h>
#include <stdlib.h>
#include "searching.h"

//support function
int max(int a, int b) 
{
  if(a>b)
    {
      return a;
    }
  else
    {
      return b;
    }
}

int height(Node* n)
{
  if (n==NULL)
    {
      return 0;
    }
  else
    {
      return n->height;
    }
}



//free the node at the end
void de_chain(Node* root)
{
  Node* current=NULL;
  Node* pre=NULL;

  current=root;
  while(current!=NULL)
    {
      pre=current;
      current=current->next;
      free(pre);
    }
}


Node *newnode(long info)
{
  Node* new=NULL;
  new=(Node*)malloc(sizeof(Node));
  if(new==NULL)
    {
      fprintf(stderr,"malloc fail\n");
      return NULL;
    }
  new->value=info;
  new->next=NULL;
  new->left=NULL;
  new->right=NULL;
  new->avl_l=NULL;
  new->avl_r=NULL;
  new->balance=0;
  new->height=0;
  return new;

}



Node *load_file(char *Filename, int *size)
{
	FILE* fptr;
	int i=0;

	long store=0;

	Node *current=NULL;
	Node *pre=NULL;
	fptr=fopen(Filename, "r");
	if(fptr==NULL)
	  {
	    return NULL;
	  }
	fseek(fptr,0,SEEK_SET);

	while(fscanf(fptr,"%ld",&store)==1)
	{
	  pre=current;
	  current=newnode(store);
	  current->next=pre;

		i++;
	}
	

	fclose(fptr);
	return current;


}

//construct the bst from the lind list
Node *Construct_BST(Node *list)
 {
   Node *current=NULL;
   Node *target=NULL;
   //Node *ptarget=NULL;
   // Node *top=NULL;
   int flag=0;
   
   current=list;
   while(current->next!=NULL)
     {
       target=list;
       current=current->next;
       flag=0;
       while(target!=NULL&&flag==0)
	 {
	   if(current->value<target->value)
	     {
	       if(target->left==NULL)
		 {
		   target->left=current;
		   flag=1;
		 }
	       else
		 {
		   target=target->left;
		 }
	     }
	   else
	     {
	       if(target->right==NULL)
		 {
		   target->right=current;
		   flag=1;
		 }
	       else
		 {
		   target=target->right;
		 }
	     }
	 }
     }
   return list;
 }


//print tree using different method

long Print_BST_BF(char *Filename, Node *root)
{
  stack s1;
  stack s2;
  Node* current;
  stack_int(&s1,1000);
  stack_int(&s2,1000);
  FILE *fptr=NULL;
  fptr=fopen(Filename,"w");
  if(fptr==NULL)
    {
      fprintf(stderr,"unable to opne the file\n");
      return -1;
    }

  int depth=0;
  stack_push(&s1,root);

  while(!stack_empty(&s1))
    {
      while(!stack_empty(&s1))
	{
	  current=stack_pop(&s1);
	  
	  fprintf(fptr,"%ld\n",current->value);
	  if(current->left!=NULL)
	    {
	      stack_push(&s2,current->left);
	    }

	  if(current->right!=NULL)
	    {
	      stack_push(&s2,current->right);
	    }
	}

      while(!stack_empty(&s2))
	{
	  stack_push(&s1,stack_pop(&s2));
	}
      depth+=1;
      //printf("depth=%d\n\n",depth);
    }


  if((&s1)!=NULL)
  stack_di(&s1);

  if((&s2)!=NULL)
  stack_di(&s2);

  fclose(fptr);

  return depth;
}

long Print_BST_Preorder(char *Filename, Node *root)
{
  stack s1;
  stack s2;
  Node* current;
  stack_int(&s1,1000);
  stack_int(&s2,1000);

  FILE *fptr=NULL;
  fptr=fopen(Filename,"w");
  if(fptr==NULL)
    {
      fprintf(stderr,"unable to opne the file\n");
      return -1;
    }

  // int depth=0;
  stack_push(&s1,root);

  while(!stack_empty(&s1))
    {
      current=stack_pop(&s1);
      fprintf(fptr,"%ld\n",current->value);

      if(current->left!=NULL)
	{
	  stack_push(&s1,current->left);
	}

      if(current->right!=NULL)
	{
	  stack_push(&s2,current->right);
	}


      if(stack_empty(&s1))
	{
	  if(!stack_empty(&s2))
	    {
	      stack_push(&s1,stack_pop(&s2));
	    }
	}

    }

  stack_di(&s1);
  stack_di(&s2);
  fclose(fptr);
  return 0;

}

long Print_BST_Inorder(char *Filename, Node *root)
{
  //int flag=0;
  stack s1;
  // stack s2;
  Node* current=NULL;
  stack_int(&s1,1000);
  // stack_int(&s2,1000);
  //int depth=0;

  FILE *fptr=NULL;
  fptr=fopen(Filename,"w");
  if(fptr==NULL)
    {
      fprintf(stderr,"unable to opne the file\n");
      return -1;
    }
  current=root;
  //stack_push(&s1,root);

  while(!stack_empty(&s1)||current!=NULL)
    {

      if (current!=NULL)
      {
	stack_push(&s1,current);
	current=current->left;
      }
      else
	{
	  current=stack_top(&s1);
	  stack_pop(&s1);
	  fprintf(fptr,"%ld\n",current->value);
	  current=current->right;
	}
    }
 
  fclose(fptr);
  stack_di(&s1);
  // stack_di(&s2);
  return 0;

}



long Print_BST_Postorder(char *Filename, Node *root)
{
  stack s1;
  stack s2;
  stack s3;
  Node* current;
  Node* current2;
  stack_int(&s1,1000);
  stack_int(&s2,1000);
  stack_int(&s3,1000);
  //int depth=0;

  FILE *fptr=NULL;
  fptr=fopen(Filename,"w");
  if(fptr==NULL)
    {
      fprintf(stderr,"unable to opne the file\n");
      return -1;
    }

  if(root==NULL)
    {
      return 0;
    }

  if(root->left==NULL&&root->right==NULL)
    {
      fprintf(fptr,"%ld\n",root->value);
    }

  if(root->left!=NULL)
    {
  stack_push(&s1,root->left);
    }


  while(!stack_empty(&s1)||!stack_empty(&s2))
    {
      if(!stack_empty(&s1)&&stack_empty(&s2))
	{
	  current=stack_pop(&s1);

	  if(current->left==NULL&&current->right==NULL)
	    {
	      fprintf(fptr,"%ld\n",current->value);
	    }
	  else
	    {
	  if(current->left!=NULL)
	    {
	      stack_push(&s1,current->left);
	    }

	  stack_push(&s2,current);
	    }
	 
	    
	}
      else if(stack_empty(&s1)&&!stack_empty(&s2))
	{
	  current=stack_pop(&s2);

	  if(current->right!=NULL)
	    {
	      stack_push(&s1,current->right);
	    }

	  stack_push(&s3,current);
	}
      else
	{

	  current=stack_pop(&s1);
	  current2=stack_pop(&s2);
	  if(current2->right!=NULL)
	    {
	      stack_push(&s1,current2->right);
	    }
	  
	  stack_push(&s3,current2);

	  if(current->left==NULL&&current->right==NULL)
	    {
	      fprintf(fptr,"%ld\n",current->value);
	    }
	  else
	    {
	  if(current->left!=NULL)
	    {
	      stack_push(&s1,current->left);
	    }
	  stack_push(&s2,current);
	    }
	  

	}

    }

  while(!stack_empty(&s3))
    {
      fprintf(fptr,"%ld\n",(stack_pop(&s3))->value);
    }

  if(root->right!=NULL)
    {
      stack_push(&s1,root->right);
 
    }
  stack_push(&s3,root);
  while(!stack_empty(&s1)||!stack_empty(&s2))
    {
      if(!stack_empty(&s1)&&stack_empty(&s2))
	{
	  current=stack_pop(&s1);

	  if(current->left==NULL&&current->right==NULL)
	    {
	      fprintf(fptr,"%ld\n",current->value);
	    }
	  else
	    {
	  if(current->left!=NULL)
	    {
	      stack_push(&s1,current->left);
	    }

	  stack_push(&s2,current);
	    }

	    
	}
      else if(stack_empty(&s1)&&!stack_empty(&s2))
	{
	  current=stack_pop(&s2);

	  if(current->right!=NULL)
	    {
	      stack_push(&s1,current->right);
	    }

	  stack_push(&s3,current);
	}
      else
	{

	  current=stack_pop(&s1);
	  current2=stack_pop(&s2);

	  if(current2->right!=NULL)
	    {
	      stack_push(&s1,current2->right);
	    }
	  
	  stack_push(&s3,current2);

	  if(current->left==NULL&&current->right==NULL)
	    {
	      fprintf(fptr,"%ld\n",current->value);
	    }
	  else
	    {
	  if(current->left!=NULL)
	    {
	      stack_push(&s1,current->left);
	    }
	  stack_push(&s2,current);
	    }
	}
    }

  while(!stack_empty(&s3))
    {
      fprintf(fptr,"%ld\n",(stack_pop(&s3))->value);
    }


  stack_di(&s1);
  stack_di(&s2);
  stack_di(&s3);
  fclose(fptr);
  return 0;


}


//inplement of avl balance tree


Node *l_rotation(Node* n)
{
  Node *n1=NULL;
  if(n==NULL)
    {
      fprintf(stderr,"null node l_r\n");
      return NULL;
    }
  n1=n->avl_l;
  n->avl_l=n1->avl_r;
  n1->avl_r=n;

  n->height=max( height(n->avl_l), height(n->avl_r))+1;
  n1->height=max( height(n1->avl_l), height(n))+1;

  return n1;
}

Node *r_rotation(Node *n)
{
  Node *n1=NULL;
  if(n==NULL)
    {
      fprintf(stderr,"null node l_r\n");
      return NULL;
    }

  n1=n->avl_r;
  n->avl_r=n1->avl_l;
  n1->avl_l=n;

  n->height=max( height(n->avl_l), height(n->avl_r))+1;
  n1->height=max( height(n1->avl_r), height(n))+1;

  return n1;

}

Node *l_r_rotation(Node *n)
{
  n->avl_l=r_rotation(n->avl_l);

  return l_rotation(n);


}

Node *r_l_rotation(Node *n)
{

  n->avl_r=l_rotation(n->avl_r);
  return r_rotation(n);
}

Node *avl_insert(Node *root, Node *target)
{
  if(target==NULL)
    {
    return NULL;
    fprintf(stderr,"none valid node_avl\n");
    }
 
  if(root==NULL)
    {
      // printf("asdadasdsadasdasdasdads\n");
      //root=target;
      //return target;
      root=target;
    }
 else  if((root)->value>target->value)
    {
      // printf("%ld,,%ld\n",root->value,target->value);

      (root)->avl_l=avl_insert(((root)->avl_l),target);

      //printf("h_d=%d,,h_l=%d,,h_r==%d\n\n",height((root)->avl_l)-height((root)->avl_r),height((root)->avl_l),height((root)->avl_r));

      if(height((root)->avl_l)-height((root)->avl_r)==2)
	{
	  if(target->value<((root)->avl_l)->value)
	    {
	      root=l_rotation(root);
	    }
	  else
	    {
	      root=l_r_rotation(root);
	    }
	}
    }
  else if((root)->value<=target->value)
    {
      // printf("%ld,,%ld\n",root->value,target->value);

      (root)->avl_r=avl_insert(((root)->avl_r),target);

      //printf("h_d=%d,,h_l=%d,,h_r==%d\n\n",height((root)->avl_r)-height((root)->avl_l),height((root)->avl_l),height((root)->avl_r));

      if(height((root)->avl_r)-height((root)->avl_l)==2)
	{
	  
	  if(target->value>=((root)->avl_r)->value)
	    {
	      root=r_rotation(root);
	    }
	  else
	    {
	      root=r_l_rotation(root);
	    }
	    }
	
    }
  else 
    {
      fprintf(stderr,"invalid node_avl  %ld\n",root->value);
    }

  (root)->height=max(height((root)->avl_l),height((root)->avl_r))+1;

  return (root);


}

  Node* Balance_BST(Node *tree)
  {
   Node *current=NULL;
   Node *head=NULL;
   current=tree;
   while(current!=NULL)
     {

       //printf("c_v=%ld\n",(current)->value);
      head= avl_insert(head,current);
 
       if(current->avl_l!=NULL)
	 {
	   //printf("c_v_l=%ld\n\n",(current->avl_l)->value);
	 }
       current=current->next;
     }

   return head;
  }

//search the node in list/tree/avl_tree


int Search_List(Node *list, long key, double *N_Comp)
{
  Node *current=NULL;
  current=list;
  while (current!=NULL)
    {
      *N_Comp+=1;
      //printf("lv=%ld,k=%ld\n",current->value,key);
      if(current->value==key)
	{
	  
	  return 1;
	}

      current=current->next;
    }

  return 0;
}

int Search_Tree(Node *root, long key, double *N_Comp)
{
  if (root==NULL)
    {
    return 0;
    }


  if(root->value==key)
    {
      *N_Comp+=1;
      return 1;
    }

  if(key<root->value)
    {
      *N_Comp+=1;
      return Search_Tree(root->left,key,N_Comp);
    }
  else
    {
      *N_Comp+=1;
      return Search_Tree(root->right,key,N_Comp);
    }


}

int Search_avl_Tree(Node *root, long key, double *N_Comp)
{
  if (root==NULL)
    {
    return 0;
    }


  if(root->value==key)
    {
      *N_Comp+=1;
      return 1;
    }

  if(key<(root->value))
    {
      *N_Comp+=1;
      return Search_avl_Tree(root->avl_l,key,N_Comp);
    }
  else
    {
      *N_Comp+=1;
      return Search_avl_Tree(root->avl_r,key,N_Comp);
    }


}

//implementation of stack

 void stack_di(stack *s)
 {
   free(s->item);
   s->item=NULL;
   s->size=0;
   s->min=0;
   s->top=-1;
 }

int stack_int(stack *s, int size)
{
   if(size<=0)
     {
       size=stack_int_size;
     }

   s->top=-1;
   s->size=size;
   s->min=size;
   s->item=(Node**)malloc(sizeof(Node*)*size);

 if(s->item==NULL)
   {
     s->size=0;
     return FALSE;
   }

 return TRUE;

}

 stack *stack_new(int size)
{
  stack* result=NULL;

  result=(stack*)malloc(sizeof(stack));

  if(result==NULL)
    {
      return NULL;
    }

  if(!stack_int(result, size))
    {
      free(result);
      return NULL;
    }

  return result;
}

 void stack_de(stack* s)
 {
   stack_di(s);
   free(s);
 }

 int stack_empty(stack *s)
 {
   return (s->top<0);
 }

 Node *stack_top(stack* s)
 {
   return (s->item[s->top]);
 }

Node *stack_pop(stack *s)
{
   Node *result=NULL;
   int new_size=0;
   Node **new_item=NULL;


   result=s->item[s->top];
   s->top=s->top-1;

   if((s->size==s->min)||((int)((s->top+1)*s_g_f*s_g_f)+1)>=s->size)
     {
       return result;
     }

   new_size=(int)((s->top+1)*s_g_f+1);

   if(new_size<=s->top+1)
     {
       return result;
     }

   if(new_size<s->min)
     {
       new_size=s->min;
     }
   new_item=(Node**)realloc(s->item, sizeof(Node*)*new_size);

   if(new_item==NULL)
     {
       return result;
     }

   s->size=new_size;
   s->item=new_item;
   return result;
 }


 int stack_push(stack*s, Node *item)
 {
   int new_size=0;
   Node **new_item=NULL;

   if(s->top>=s->size-1)
     {
       new_size=(int)(s_g_f*s->size)+1;
       if(new_size<=s->size)
	 {
	   return FALSE;
	 }

       new_item=(Node**)realloc(s->item,sizeof(Node*)*new_size);

       if(new_item==NULL)
	 {
	 return FALSE;
	 }


       s->size=new_size;
       s->item=new_item;
     }

   s->top=s->top+1;
   s->item[s->top]=item;
   return TRUE;


 }

long Print_avlBST_BF(char *Filename, Node *root)
{
 //int flag=0;
  stack s1;
  // stack s2;
  Node* current=NULL;
  stack_int(&s1,1000);
  // stack_int(&s2,1000);
  //int depth=0;

  FILE *fptr=NULL;
  fptr=fopen(Filename,"w");
  if(fptr==NULL)
    {
      fprintf(stderr,"unable to opne the file\n");
      return -1;
    }
  current=root;
  //stack_push(&s1,root);

  while(!stack_empty(&s1)||current!=NULL)
    {

      if (current!=NULL)
      {
	stack_push(&s1,current);
	current=current->avl_l;
      }
      else
	{
	  current=stack_top(&s1);
	  stack_pop(&s1);
	  fprintf(fptr,"%ld\n",current->value);
	  current=current->avl_r;
	}
    }
 
  fclose(fptr);
  stack_di(&s1);
  // stack_di(&s2);
  return 0;
}




 
